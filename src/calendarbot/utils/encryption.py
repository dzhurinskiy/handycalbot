"""Token encryption utilities."""

from cryptography.fernet import Fernet

from calendarbot.config import get_settings


class TokenEncryption:
    """Encrypt and decrypt OAuth tokens."""

    def __init__(self) -> None:
        settings = get_settings()
        if not settings.encryption_key:
            raise ValueError("ENCRYPTION_KEY must be set in environment")
        self.fernet = Fernet(settings.encryption_key.encode())

    def encrypt(self, plaintext: str) -> str:
        """Encrypt a string."""
        return self.fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        """Decrypt a string."""
        return self.fernet.decrypt(ciphertext.encode()).decode()


def generate_encryption_key() -> str:
    """Generate a new Fernet encryption key."""
    return Fernet.generate_key().decode()
