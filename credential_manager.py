import keyring
import cryptography
from cryptography.fernet import Fernet

class CredentialManager:
    def __init__(self, service_name):
        self.service_name = service_name
        self.key = self.load_key()
        self.fernet = Fernet(self.key)

    def load_key(self):
        # Load the previously generated key
        return keyring.get_password('keyring_service', 'encryption_key')

    def save_key(self):
        # Generate a new key and save it to keyring
        key = Fernet.generate_key()
        keyring.set_password('keyring_service', 'encryption_key', key.decode())
        return key

    def encrypt(self, credential):
        return self.fernet.encrypt(credential.encode()).decode()

    def decrypt(self, encrypted_credential):
        return self.fernet.decrypt(encrypted_credential.encode()).decode()

    def store_credential(self, identifier, credential):
        encrypted_credential = self.encrypt(credential)
        keyring.set_password(self.service_name, identifier, encrypted_credential)

    def retrieve_credential(self, identifier):
        encrypted_credential = keyring.get_password(self.service_name, identifier)
        if encrypted_credential:
            return self.decrypt(encrypted_credential)
        return None

    def delete_credential(self, identifier):
        keyring.delete_password(self.service_name, identifier)