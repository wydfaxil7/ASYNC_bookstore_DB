# test_hash.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

password = "my_very_secure_password_1234567890"
hashed = pwd_context.hash(password[:72])  # truncate manually if needed
print("Hashed password:", hashed)

is_valid = pwd_context.verify(password[:72], hashed)
print("Password valid?", is_valid)