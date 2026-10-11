import hashlib
import secrets


def hash_password(password: str) -> str:
    """使用SHA256+随机盐加密密码"""
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return f"{salt}:{hashed}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    salt, stored_hash = hashed_password.split(":")
    computed_hash = hashlib.sha256(f"{salt}{plain_password}".encode()).hexdigest()
    return secrets.compare_digest(computed_hash, stored_hash)