#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import base64
import hashlib
import json
import random
import secrets
import sys
import urllib.request
import urllib.error

from Cryptodome.Cipher import AES, PKCS1_v1_5
from Cryptodome.PublicKey import RSA


class NVRClient:
    DISK_QUERIES = [
        ("getinfo", "StorageInfo"),
        ("getinfo", "HddInfo"),
        ("getinfo", "HDDInfo"),
        ("getinfo", "DiskInfo"),
        ("getconfig", "StorageInfo"),
        ("getconfig", "HddInfo"),
        ("getconfig", "HDDInfo"),
        ("getconfig", "DiskInfo"),
        ("getconfig", "Storage.StorageInfo"),
        ("getconfig", "Storage.HddInfo"),
        ("getconfig", "Storage.HDDInfo"),
        ("getconfig", "Storage.DiskInfo"),
        ("getconfig", "Record.Storage"),
        ("getconfig", "Record.HDD"),
    ]

    def __init__(self, host, user, password, port=80, timeout=10, oem_header=""):
        self.host = host
        self.port = int(port)
        self.user = user
        self.password = password
        self.timeout = int(timeout)
        self.oem_header = oem_header or ""

        self.base_url = f"http://{self.host}:{self.port}/cgi-bin"

        self.salt = None
        self.session_id = None
        self.aes_enabled = False
        self.aes_key = None
        self.aes_key_bytes = None
        self.aes_iv = b"\x00" * 16

    @staticmethod
    def md5_hex(value):
        return hashlib.md5(str(value).encode("utf-8")).hexdigest()

    @staticmethod
    def md5_8(value):
        return NVRClient.md5_hex(value)[:8]

    @staticmethod
    def random_ascii16():
        return "".join(chr(random.randint(48, 90)) for _ in range(16))

    @staticmethod
    def zero_pad(data, block_size=16):
        rem = len(data) % block_size
        if rem:
            data += b"\x00" * (block_size - rem)
        return data

    @staticmethod
    def zero_unpad(data):
        return data.rstrip(b"\x00")

    @staticmethod
    def make_rsa_key(public_key_string):
        parts = public_key_string.split(",")
        if len(parts) < 2:
            raise RuntimeError(f"Bad RSA PublicKey format: {public_key_string}")
        n = int(parts[0].strip(), 16)
        e = int(parts[1].strip(), 16)
        return RSA.construct((n, e))

    @staticmethod
    def rsa_encrypt_hex(rsa_key, text):
        cipher = PKCS1_v1_5.new(rsa_key)
        encrypted = cipher.encrypt(str(text).encode("utf-8"))
        return encrypted.hex()

    def aes_encrypt_b64(self, payload):
        if not self.aes_key_bytes:
            raise RuntimeError("AES key is empty")
        raw = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        raw = self.zero_pad(raw)
        cipher = AES.new(self.aes_key_bytes, AES.MODE_CBC, self.aes_iv)
        encrypted = cipher.encrypt(raw)
        return base64.b64encode(encrypted).decode("ascii")

    def aes_decrypt_text(self, value):
        if not self.aes_key_bytes:
            raise RuntimeError("AES key is empty")
        cleaned = value.strip()
        encrypted = base64.b64decode(cleaned)
        cipher = AES.new(self.aes_key_bytes, AES.MODE_CBC, self.aes_iv)
        decrypted = cipher.decrypt(encrypted)
        return self.zero_unpad(decrypted).decode("utf-8", errors="replace")

    def post(self, cgi_name, payload, use_aes=None, timeout=None):
        if use_aes is None:
            use_aes = self.aes_enabled

        timeout = timeout or self.timeout
        url = f"{self.base_url}/{cgi_name}.cgi"

        if use_aes:
            body = self.aes_encrypt_b64(payload).encode("utf-8")
            content_type = "text/plain;charset=utf-8"
        else:
            body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
            content_type = "application/json;charset=utf-8"

        req = urllib.request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "Content-Type": content_type,
                "User-Agent": "Zabbix-NVR-Monitor/1.0",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                raw = response.read().decode("utf-8", errors="replace").strip()
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace").strip()
            raise RuntimeError(f"HTTP {e.code} from {url}: {error_body}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Cannot connect to {url}: {e}")

        if use_aes:
            try:
                decoded = json.loads(raw)
                if isinstance(decoded, dict):
                    return decoded
            except Exception:
                pass
            raw = self.aes_decrypt_text(raw)

        try:
            return json.loads(raw)
        except Exception as e:
            raise RuntimeError(f"Cannot parse response from {cgi_name}. Error: {e}. Raw: {raw}")

    def send_v2(self, cgi_name, payload, use_aes=None, timeout=None):
        if cgi_name != "resetpwd":
            if not self.salt:
                raise RuntimeError("Salt is empty")
            payload["Salt"] = self.salt
        return self.post(cgi_name, payload, use_aes=use_aes, timeout=timeout)

    def login(self):
        salt_resp = self.post("login", {"Name": "GetSalt"}, use_aes=False)

        if salt_resp.get("Ret") != 100:
            raise RuntimeError(f"GetSalt failed: {json.dumps(salt_resp, ensure_ascii=False)}")

        self.salt = salt_resp.get("Salt")
        login_type = salt_resp.get("LoginEncryptionType", "")
        data_type = salt_resp.get("DataEncryptionType", "")

        login_payload = {"Name": "Login"}

        if "RSA" in login_type:
            rsa_key = self.make_rsa_key(salt_resp.get("PublicKey", ""))

            login_payload["LoginEncryptionType"] = "RSA"
            login_payload["User"] = self.rsa_encrypt_hex(rsa_key, self.user)

            sign_plain = self.oem_header + self.salt + self.md5_hex(self.password)
            login_payload["Sign"] = self.rsa_encrypt_hex(rsa_key, sign_plain)

            hex_data = secrets.token_hex(48)
            login_payload["VERK"] = self.rsa_encrypt_hex(rsa_key, hex_data)

            if data_type == "AES":
                self.aes_key = self.random_ascii16()
                self.aes_key_bytes = self.aes_key.encode("utf-8")
                login_payload["DTAK"] = self.rsa_encrypt_hex(rsa_key, self.aes_key)
        else:
            login_payload["LoginEncryptionType"] = "MD5_8"
            login_payload["User"] = self.user
            login_payload["Sign"] = self.md5_8(
                self.salt + self.oem_header + self.md5_8(self.password)
            )

        login_resp = self.send_v2("login", login_payload, use_aes=False)

        if login_resp.get("Ret") != 100:
            raise RuntimeError(f"Login failed: {json.dumps(login_resp, ensure_ascii=False)}")

        self.session_id = login_resp.get("SessionID")
        self.aes_enabled = (data_type == "AES")

    def logout(self):
        if not self.salt:
            return
        try:
            self.send_v2("login", {"Name": "Logout"}, use_aes=self.aes_enabled, timeout=3)
        except Exception:
            pass

    def session_hex(self):
        sid = self.session_id
        if isinstance(sid, str):
            if sid.startswith("0x"):
                return sid
            try:
                n = int(sid, 16)
            except ValueError:
                n = int(sid)
        else:
            n = int(sid or 0)
        return f"0x{n & 0xFFFFFFFF:08x}"

    def get_config(self, name, timeout=None):
        payload = {
            "Name": name,
            "SessionID": self.session_hex(),
        }
        return self.send_v2("getconfig", payload, use_aes=self.aes_enabled, timeout=timeout)

    def get_info(self, name, timeout=None):
        payload = {
            "Name": name,
            "SessionID": self.session_hex(),
        }
        return self.send_v2("getinfo", payload, use_aes=self.aes_enabled, timeout=timeout)

def normalize_channels(raw):
    arr = raw.get("NetWork.ChnStatus", [])
    if not isinstance(arr, list):
        return []

    channels = []
    for i, ch in enumerate(arr):
        if not isinstance(ch, dict):
            continue
        name = ch.get("ChnName", "")
        if not name:
            continue
        channels.append({
            "index": i,
            "name": name,
            "status": ch.get("Status", ""),
            "curres": ch.get("CurRes", ""),
            "maxres": ch.get("MaxRes", ""),
            "active": ch.get("Status") != "NoConfig",
        })
    return channels


def normalize_system(raw):
    name = raw.get("Name")
    data = raw.get(name, {}) if name else {}
    if not isinstance(data, dict):
        data = {}
    return {
        "name": name,
        "ret": raw.get("Ret"),
        "data": data,
    }


def normalize_disks(raw):
    name = raw.get("Name")
    data = raw.get(name) if name else None
    if data is None:
        return []
    if isinstance(data, list):
        disks = data
    elif isinstance(data, dict):
        disks = [data]
    else:
        return []

    result = []
    for i, disk in enumerate(disks):
        if not isinstance(disk, dict):
            continue
        item = dict(disk)
        if "index" not in item:
            item["index"] = i
        result.append(item)
    return result


def collect_disks(client):
    for cgi, name in NVRClient.DISK_QUERIES:
        try:
            if cgi == "getinfo":
                raw = client.get_info(name, timeout=5)
            else:
                raw = client.get_config(name, timeout=5)
            if raw.get("Ret") == 100:
                disks = normalize_disks(raw)
                if disks:
                    return disks
        except Exception:
            continue
    return []


def collect(client):
    result = {
        "system": {},
        "channels": [],
        "disks": [],
        "errors": [],
    }

    client.login()

    try:
        ch_raw = client.get_config("NetWork.ChnStatus")
        result["channels"] = normalize_channels(ch_raw)
    except Exception as e:
        result["errors"].append({"section": "channels", "error": str(e)})

    try:
        sys_raw = client.get_info("SystemInfo")
        result["system"] = normalize_system(sys_raw)
    except Exception as e:
        result["errors"].append({"section": "system", "error": str(e)})

    try:
        result["disks"] = collect_disks(client)
    except Exception as e:
        result["errors"].append({"section": "disks", "error": str(e)})

    return result


def main():
    parser = argparse.ArgumentParser(description="NVR monitor for Zabbix")
    parser.add_argument("--host", required=True)
    parser.add_argument("--user", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--port", default=80, type=int)
    parser.add_argument("--timeout", default=10, type=int)
    parser.add_argument("--oem-header", default="")
    args = parser.parse_args()

    client = NVRClient(
        host=args.host,
        user=args.user,
        password=args.password,
        port=args.port,
        timeout=args.timeout,
        oem_header=args.oem_header,
    )

    try:
        data = collect(client)
        print(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    except Exception as e:
        print(json.dumps({
            "system": {},
            "channels": [],
            "disks": [],
            "errors": [{"section": "main", "error": str(e)}],
        }, ensure_ascii=False, separators=(",", ":")))
        sys.exit(1)
    finally:
        client.logout()


if __name__ == "__main__":
    main()