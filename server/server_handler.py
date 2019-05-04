from db import Database
from typing import Optional
from encryption import AESCipher
from pdf import PdfHandler


class ServerHandler:
    def __init__(self):
        self._db = Database()
        self._cipher = AESCipher()

    def get_user_id(self, email: str) -> Optional[str]:
        sql = "SELECT id FROM users WHERE unique_id=%s"

        with self._db as _db:
            result = _db.select_with_params(sql, [email, ])

        if result:
            return result[0][0]
        return None

    def login_user(self, email: str, password: str) -> any:
        user_id = self.get_user_id(email)

        if user_id:
            user_pwd = self._get_user_password(user_id)

            if user_pwd:
                decrypted_pwd = self._cipher.decrypt(user_pwd)

                if decrypted_pwd == password:
                    return self._update_login(user_id)
                return 0, 'Invalid Password'
        return 0, "Invalid User ID"

    def _update_login(self, user_id: str) -> any:
        sql = "UPDATE login SET active=1 WHERE user_id=%s"

        with self._db as _db:
            _db.update(sql, [user_id, ])
        return 1, 'Success'

    def is_logged_in(self, user_id: str) -> bool:
        sql = "SELECT active FROM login WHERE user_id=%s"

        with self._db as _db:
            result = _db.select_with_params(sql, [user_id, ])

        if result:
            if result[0][0] == '1' or result[0][0] == 1:
                return True
        return False

    def logout(self, user_id: str) -> None:
        sql = "UPDATE login SET active=0 WHERE user_id=%s"

        with self._db as _db:
            _db.update(sql, [user_id, ])

    def _get_user_password(self, user_id: str) -> any:
        sql = "SELECT password_hash FROM login WHERE user_id=%s"

        with self._db as _db:
            result = _db.select_with_params(sql, [user_id, ])

        if result[0][0]:
            return result[0][0]
        else:
            return None

    def get_security_questions(self):
        sql = "SELECT * FROM questions"

        with self._db as _db:
            result = _db.select(sql)

        return result if result else None

    def create_user(self, user_obj: dict) -> any:
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

    def check_if_user_exists(self, email: str) -> bool:
        sql = "SELECT id FROM users WHERE unique_id=%s"

        with self._db as _db:
            result = _db.select_with_params(sql, [email, ])
        if result and result[0][0]:
            return True
        return False

    def store_security_questions(self, user_id: str, question_obj: any):
        sql = """INSERT INTO user_security (user_id, question_id, answer_text)
                 VALUES(%s, %s, %s)"""

        with self._db as _db:
            for obj in question_obj:
                _db.insert(sql, [user_id, obj[0], obj[1], ])

    def write_acknowledgement_page(self, title: str, acknowledgement: str, page: str, user_id: str):
        page_name = 'page_{}'.format(page)
        pdf_writer = PdfHandler(page_name, user_id)
        pdf_writer.set_document_title(title)
        success = pdf_writer.write_document(acknowledgement)

        return success

    def write_page(self, text: str, page: str, user_id: str) -> any:
        page_name = 'page_{}'.format(page)
        pdf_writer = PdfHandler(page_name, user_id)
        success = pdf_writer.write_document(text)

        return success

    def get_saved_progress(self, user_id: str) -> any:
        sql = """SELECT
                    story_id,
                    last_page,
                    page_type
                 FROM user_progress
                 WHERE user_id = %s
                    AND complete = 0"""

        with self._db as _db:
            result = _db.select_with_params(sql, user_id)
        if result:
            return {
                'story_id': result[0][0],
                'last_page': result[0][1],
                'page_type': result[0][2]
            }
        else:
            return None


if __name__ == '__main__':
    test = ServerHandler()
    user = {
        'email': 'test@test.com',
        'name': 'Test',
        'lastname': 'McTest',
        'address': '1234 Some street',
        'address2': '',
        'city': 'Canton',
        'state': 'MI',
        'zip': '48188',
        'password': 'IamKing'
    }

    new = test.create_user(user)
    print("NEW USER ID: {0}".format(new))