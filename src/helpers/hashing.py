import bcrypt


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        verified = bcrypt.checkpw(
            plain_password.encode(), hashed_password.encode())
        return verified

    @staticmethod
    def get_password_hash(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
