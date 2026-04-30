# -*- coding: utf-8 -*-
# @Time : 2026/4/30 17:13
# @Author : stone


import base64
import json
import random
import string
import textwrap
from typing import Any, Dict, Tuple, Union

from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA

ENCRYPT_HEADER = "encrypt-key"


def generate_random_string(length: int = 32) -> str:
    """
    对应前端 generateRandomString()
    生成 32 位随机 AES Key 字符串。
    """
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    """
    AES PKCS7 Padding
    """
    pad_len = block_size - len(data) % block_size
    return data + bytes([pad_len]) * pad_len


def pkcs7_unpad(data: bytes) -> bytes:
    """
    AES PKCS7 UnPadding
    """
    if not data:
        raise ValueError("解密结果为空，无法去除 PKCS7 Padding")

    pad_len = data[-1]

    if pad_len < 1 or pad_len > AES.block_size:
        raise ValueError("PKCS7 Padding 不合法")

    return data[:-pad_len]


def rsa_encrypt_by_public_key(text: str, public_key_pem: str) -> str:
    """
    对应前端 encrypt(txt)
    使用 RSA 公钥加密，返回 Base64 字符串。

    JSEncrypt 默认使用 PKCS#1 v1.5 padding。
    """
    public_key = RSA.import_key(public_key_pem)
    cipher = PKCS1_v1_5.new(public_key)

    encrypted_bytes = cipher.encrypt(text.encode("utf-8"))

    return base64.b64encode(encrypted_bytes).decode("utf-8")


def rsa_decrypt_by_private_key(encrypted_text: str, private_key_pem: str) -> str:
    """
    对应前端 decrypt(txt)
    使用 RSA 私钥解密 Base64 密文。
    """
    private_key = RSA.import_key(private_key_pem)
    cipher = PKCS1_v1_5.new(private_key)

    encrypted_bytes = base64.b64decode(encrypted_text)
    sentinel = b"__RSA_DECRYPT_ERROR__"

    decrypted_bytes = cipher.decrypt(encrypted_bytes, sentinel)

    if decrypted_bytes == sentinel:
        raise ValueError("RSA 解密失败，请检查私钥或密文")

    return decrypted_bytes.decode("utf-8")


def aes_encrypt_ecb_pkcs7(message: Union[str, Dict, list], aes_key: Union[str, bytes]) -> str:
    """
    对应前端 encryptWithAes(message, aesKey)

    前端逻辑：
    CryptoJS.AES.encrypt(message, aesKey, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    }).toString()

    返回 Base64 格式 AES 密文。
    """
    if isinstance(message, (dict, list)):
        message = json.dumps(message, ensure_ascii=False, separators=(",", ":"))

    if not isinstance(message, str):
        message = str(message)

    if isinstance(aes_key, str):
        aes_key = aes_key.encode("utf-8")

    cipher = AES.new(aes_key, AES.MODE_ECB)

    plain_bytes = message.encode("utf-8")
    padded_bytes = pkcs7_pad(plain_bytes)

    encrypted_bytes = cipher.encrypt(padded_bytes)

    return base64.b64encode(encrypted_bytes).decode("utf-8")


def aes_decrypt_ecb_pkcs7(encrypted_message: str, aes_key: Union[str, bytes]) -> str:
    """
    对应前端 decryptWithAes(message, aesKey)

    encrypted_message 是 Base64 格式的 AES 密文。
    """
    if isinstance(aes_key, str):
        aes_key = aes_key.encode("utf-8")

    cipher = AES.new(aes_key, AES.MODE_ECB)

    encrypted_bytes = base64.b64decode(encrypted_message)
    decrypted_padded_bytes = cipher.decrypt(encrypted_bytes)

    decrypted_bytes = pkcs7_unpad(decrypted_padded_bytes)

    return decrypted_bytes.decode("utf-8")


def encrypt_request_data(
        data: Any,
        public_key_pem: str,
) -> Tuple[Dict[str, str], str]:
    """
    请求加密函数。

    返回：
    headers: {"encrypt-key": "..."}
    encrypted_body: AES 加密后的请求体字符串

    对应前端请求拦截器里的逻辑：
    1. 生成 AES key
    2. Base64(AES key)
    3. RSA 公钥加密 Base64(AES key)
    4. 请求体使用 AES 加密
    """
    aes_key = generate_random_string(32)

    aes_key_base64 = base64.b64encode(aes_key.encode("utf-8")).decode("utf-8")

    encrypted_aes_key = rsa_encrypt_by_public_key(
        text=aes_key_base64,
        public_key_pem=public_key_pem,
    )

    if isinstance(data, (dict, list)):
        plain_text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    else:
        plain_text = str(data)

    encrypted_body = aes_encrypt_ecb_pkcs7(
        message=plain_text,
        aes_key=aes_key,
    )

    headers = {
        ENCRYPT_HEADER: encrypted_aes_key
    }

    return headers, encrypted_body


def decrypt_response_data(
        encrypted_body: str,
        encrypted_key: str,
        private_key_pem: str,
        parse_json: bool = True,
) -> Any:
    """
    响应解密函数。

    参数：
    encrypted_body: 响应体 response.data
    encrypted_key: 响应头 encrypt-key
    private_key_pem: RSA 私钥

    对应前端响应拦截器里的逻辑：
    1. RSA 私钥解密 encrypt-key
    2. 得到 Base64(AES key)
    3. Base64 解码得到 AES key
    4. AES 解密响应体
    5. JSON.parse
    """
    aes_key_base64 = rsa_decrypt_by_private_key(
        encrypted_text=encrypted_key,
        private_key_pem=private_key_pem,
    )

    aes_key = base64.b64decode(aes_key_base64).decode("utf-8")

    decrypted_text = aes_decrypt_ecb_pkcs7(
        encrypted_message=encrypted_body,
        aes_key=aes_key,
    )

    if parse_json:
        return json.loads(decrypted_text)

    return decrypted_text
def build_encrypted_login_payload(
        username: str,
        password: str,
        public_key_pem: str,
) -> Tuple[Dict[str, str], str]:
    login_data = {
        "username": username,
        "password": password,
    }

    return encrypt_request_data(
        data=login_data,
        public_key_pem=public_key_pem,
    )

if __name__ == '__main__':
    publicKey = "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKoR8mX0rGKLqzcWmOzbfj64K8ZIgOdHnzkXSOVOZbFu/TJhZ7rFAN+eaGkl3C4buccQd/EjEsj9ir7ijT7h96MCAwEAAQ=="
    privateKey = "MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAmc3CuPiGL/LcIIm7zryCEIbl1SPzBkr75E2VMtxegyZ1lYRD+7TZGAPkvIsBcaMs6Nsy0L78n2qh+lIZMpLH8wIDAQABAkEAk82Mhz0tlv6IVCyIcw/s3f0E+WLmtPFyR9/WtV3Y5aaejUkU60JpX4m5xNR2VaqOLTZAYjW8Wy0aXr3zYIhhQQIhAMfqR9oFdYw1J9SsNc+CrhugAvKTi0+BF6VoL6psWhvbAiEAxPPNTmrkmrXwdm/pQQu3UOQmc2vCZ5tiKpW10CgJi8kCIFGkL6utxw93Ncj4exE/gPLvKcT+1Emnoox+O9kRXss5AiAMtYLJDaLEzPrAWcZeeSgSIzbL+ecokmFKSDDcRske6QIgSMkHedwND1olF8vlKsJUGK3BcdtM8w4Xq7BpSBwsloE="

    publicKey = "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKoR8mX0rGKLqzcWmOzbfj64K8ZIgOdHnzkXSOVOZbFu/TJhZ7rFAN+eaGkl3C4buccQd/EjEsj9ir7ijT7h96MCAwEAAQ=="

    publicKeyPem = (
            "-----BEGIN PUBLIC KEY-----\n"
            + "\n".join(textwrap.wrap(publicKey, 64))
            + "\n-----END PUBLIC KEY-----"
    )
    ast = build_encrypted_login_payload(username='superAdmin',password='Tk@2026520.',public_key_pem=publicKeyPem)
    print(ast)

