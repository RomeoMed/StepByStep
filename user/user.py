from db import Database
from auth import Auth
from encryption import AESCipher

class User(object):
    def __init__(self, email: str):
        self._db = Database()
        self._email = email
        self._cipher = AESCipher()
        self._init_tables()

    def _init_tables(self) -> None:
        sql = "CREATE TABLE IF NOT EXISTS"
        tables = ['users', 'login', 'user_security']
        #with self._db as _db:
        #TODO: create tables on init for all classes/tables
        print('hi')

    def exists_user(self) -> bool:
        sql = "SELECT id FROM users WHERE unique_id=%s"

        with self._db as _db:
            result = _db.select_with_params(sql, [self._email, ])
        if result and result[0][0]:
            return True
        return False

    def get_user_id(self) -> any:
        sql = "SELECT id FROM users WHERE unique_id=%s"

        with self._db as _db:
            result = _db.select_with_params(sql, [self._email, ])

        if result:
            return result[0][0]
        return None

    def login(self, password: str) -> any:
        user_id = self.get_user_id()

        if user_id:
            user_pwd = self._get_user_password(user_id)

            if user_pwd:
                decrypted_pwd = self._cipher.decrypt(user_pwd)

                if decrypted_pwd == password:
                    return self._update_login(user_id)
                return 0, 'Invalid Password'
        return 0, "Invalid User ID"

    def _get_user_password(self, user_id: str) -> any:
        sql = "SELECT password_hash FROM login WHERE user_id=%s"

        with self._db as _db:
            result = _db.select_with_params(sql, [user_id, ])

        if result[0][0]:
            return result[0][0]
        else:
            return None

    def _update_login(self, user_id: str) -> any:
        sql = "UPDATE login SET active=1 WHERE user_id=%s"

        with self._db as _db:
            _db.update(sql, [user_id, ])
        return 1, 'Success'

    def _logged_in_check(self, user_id: str) -> bool:
        sql = "SELECT active FROM login WHERE user_id=%s"

        with self._db as _db:
            result = _db.select_with_params(sql, [user_id, ])

        if result:
            if result[0][0] == '1' or result[0][0] == 1:
                return True
        return False

    def logout(self) -> None:
        user_id = self.get_user_id()
        sql = "UPDATE login SET active=0 WHERE user_id=%s"

        with self._db as _db:
            _db.update(sql, [user_id, ])

    def create_new_user(self, user_obj: any) -> any:
        params = [user_obj.get('email'), user_obj.get('name'), user_obj.get('lastname'),
                  user_obj.get('address'), user_obj.get('address2'), user_obj.get('city'),
                  user_obj.get('state'), user_obj.get('zip'), ]
        password = user_obj.get('password')

        sql = """INSERT INTO users (unique_id, first_name, last_name, address, address2,
                                    city, state, zip_code)
                  VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""

        with self._db as _db:
            new_id = _db.insert(sql, params)

        if new_id:
            self._create_login(new_id, password)
            return 1, new_id
        return 0, 'Unable to Create User'

    def _create_login(self, user_id: str, password: str) -> any:
        pwd_hash = self._cipher.encrypt(password)
        sql = """INSERT INTO login (user_id, password_hash, active)
                 VALUES(%s, %s, 1)"""

        with self._db as _db:
            _db.insert(sql, [user_id, pwd_hash, ])

    def insert_security_questions(self, question_obj: any) -> None:
        sql = """INSERT INTO user_security (user_id, question_id, answer_text)
                 VALUES(%s, %s, %s)"""
        user_id = self.get_user_id()
        with self._db as _db:
            for obj in question_obj:
                _db.insert(sql, [user_id, obj[0], obj[1], ])