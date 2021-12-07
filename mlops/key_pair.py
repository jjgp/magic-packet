import os

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def read_pem_public_key(pem_private_key_path, password=None):
    key_path = os.path.expanduser(pem_private_key_path)
    with open(key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password)
        public_key = private_key.public_key()
        public_bytes = public_key.public_bytes(
            serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH
        )
        return public_bytes.decode("utf-8")


def write_pem_private_key(pem_private_key_path, password=None):
    key_path = os.path.expanduser(pem_private_key_path)
    with open(key_path, "wb") as key_file:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        encryption_algorithm = (
            serialization.BestAvailableEncryption(password)
            if password
            else serialization.NoEncryption()
        )
        key_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=encryption_algorithm,
            )
        )
