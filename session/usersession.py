from api import StepAPI
from db import Database
from datetime import datetime
import json


class UserSession:
    def __init__(self, user: str):
        self._db = Database()
        self._user = user

    def get_content(self) -> any:
        sql = """SELECT id, saved_step, saved_part
                FROM user_story WHERE user_id = %s 
                AND complete = 0"""
        with self._db as _db:
            result = _db.select_with_params(sql, [self._user, ])
        if result:
            story_id = result[0][0]
            step = result[0][1]
            section = result[0][2]
        else:
            step = 1
            section = 1
            story_id = self.create_new_story(self._user)

        return self._get_display_content(step, section, story_id)

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

    def _get_display_content(self, step: int, section: int, story_id: int):
        step_num = step
        step = 'step_' + str(step)
        section_str = 'section_' + str(section)

        with open('./content/instructions.json', encoding="utf8") as f:
            content = json.load(f)

        response = {}
        if content:
            response['story_id'] = story_id
            response['title'] = content[step]['title']
            response['subtitle'] = content[step]['subtitle']
            response['section_name'] = content[step][section_str]['name']
            response['body'] = content[step][section_str]['description']
            response['step'] = step_num
            response['section'] = section
        else:
            response['message'] = "Error getting content"
        return response

    def update_content(self, step: int, section: int, story_id: int):
        response = self.check_exists_next_section(step, section, story_id)
        #TODO: updated DB
        return response

    def check_exists_next_section(self, step: int, section: int, story_id: int):
        current_step = 'step_' + str(step)
        future_section = 'section_' + str(section + 1)
        future_step = 'step_' + str(step + 1)
        with open('./content/instructions.json', encoding='utf-8') as f:
            content = json.load(f)
        try:
            content[current_step][future_section]
            return self._get_display_content(step, section + 1, story_id)
        except KeyError:
            try:
                content[future_step]
                return self._get_display_content(step + 1, 1, story_id)
            except KeyError:
                print("complete")

    def get_active_step(self):
        self._active_step -= 1

        return self.get_content()

    def set_next_step(self):
        self._active_step += 1

    def set_next_section(self):
        self._section += 1

    def set_previous_section(self):
        self._section -= 1
