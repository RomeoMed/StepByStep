from db import Database
from datetime import datetime


class StepAPI:
    def __init__(self):
        self._db = Database()

    def login_user(self, usr: str, psw: str) -> any:
        with self._db as _db:
            sql = """SELECT user_id, password_hash, locked_out,
                            active_story_id, active_step 
                     FROM login WHERE user_id = %s"""
            result = _db.select_with_params(sql, [usr,])

        return_obj = {}
        if result:
            if usr == result[0][0] and psw == result[0][1]\
                    and result[0][2] != 1:
                return_obj['status'] = 200
                return_obj['message'] = 'logged_id'
                return_obj['active_story'] = result[0][3] or None
                return_obj['active_step'] = result[0][4] or 1
            else:
                return_obj['status'] = 401
                return_obj['message'] = 'Unauthorized Access'
        else:
            return_obj['status'] = 400
            return_obj['message'] = 'User not found'
        return return_obj

    def create_new_story(self, user: str) -> int:
        sql = """INSERT INTO user_story (user_id, created_date)
                 VALUES(%s, %s)"""
        date = datetime.now()
        with self._db as _db:
            _db.insert(sql, [user, date,])
        return self._get_new_story_id(user)

    def _get_new_story_id(self, user: str) -> int:
        sql = """SELECT MAX(id) from user_story
                WHERE user_id = %s AND complete = 0"""
        with self._db as _db:
            story_id = _db.select_with_params(sql, [user,])
        return story_id

