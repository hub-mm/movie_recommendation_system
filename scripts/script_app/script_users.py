# ./scripts/scripts_app/script_users.py
import bcrypt


class User:
    user_base = {}
    user_id_counter = 1

    def __init__(self, email, username, password):
        self.user_id = User.user_id_counter
        self.email = email
        self.username = username.lower()
        self.password = self.hash_password(password)
        User.user_base[self.user_id] = self
        User.user_id_counter += 1

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)

    @classmethod
    def create_user(cls, email, username, password):
        if any(user.email == email or user.username == username for user in cls.user_base.values()):
            raise ValueError('User with this email or username already exists.')
        return cls(email, username, password)

    @classmethod
    def verify_password(cls, password, hashed_password):
        return bcrypt.checkpw(password.encode(), hashed_password)

    @classmethod
    def authenticate(cls, username, password):
        for user in cls.user_base.values():
            if user.username == username.lower() and cls.verify_password(password, user.password):
                return user
        raise ValueError('Invalid username or password.')

    @classmethod
    def update_user(cls, username, email=None, new_username=None, password=None):
        for user in cls.user_base.values():
            if user.username == username.lower():
                if email:
                    user.email = email
                if new_username:
                    user.username = new_username.lower()
                if password:
                    user.password = cls.hash_password(password)
                return user
        raise ValueError('User not found.')

    @classmethod
    def delete_user(cls, username):
        for user_id, user in list(cls.user_base.items()):
            if user.username == username.lower():
                del cls.user_base[user_id]
                return
        raise ValueError('User not found.')

    @classmethod
    def get_user(cls, username):
        for user in cls.user_base.values():
            if user.username == username.lower():
                return user
        raise ValueError('User not found.')

    def __repr__(self):
        return f"User(user_id={self.user_id}, email={self.email}, username:{self.username}"