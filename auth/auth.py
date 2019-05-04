import json
from db import Database


class Auth:
    def __init__(self):
        self._db = Database()
        self._user_id = ''
        self._pwd = ''
        with open('secret.json') as shh:
            self._secret = json.load(shh)

    def login(self, user: str, pwd: str) -> any:
        if not user or not pwd:
            return 0, 'missing_' + user if not user else pwd
        else:
            with self._db as _db:
                sql = """SELECT user_id, password_hash, locked_out,
                                active_story_id, active_step 
                         FROM login WHERE user_id = %s"""
                result = _db.select_with_params(sql, [user,])
            if not result:
                return 0, 'not_registered'
            elif result[0][2]:
                return 0, "locked_out"
            elif result[0][1] != pwd:
                return 0, "Invalid password"
            else:
                return 1, "logged_in"
