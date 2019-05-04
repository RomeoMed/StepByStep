from db import Database


class Story:
    def __init__(self, user_id: str):
        self._db = Database()
        self._user_id = user_id

    def create_new_story(self, title: str) -> any:
        sql = """INSERT INTO story (user_id, title, submitted)
                  VALUES(%s, %s, %s)"""

        with self._db as _db:
            story_id = _db.insert(sql, [self._user_id, title, 0, ])
        if story_id:
            self.save_progress(story_id, str(0), 'acknowledgement')
            return story_id
        else:
            return None

    def save_progress(self, story_id: str, page_num: str, page_type: str) -> None:
        sql = """INSERT INTO user_progress 
                (story_id, user_id, last_page, page_type)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    last_page = VALUES(last_page),
                    page_type = VALUES(page_type)
                """

        if story_id is None:
            story_id = self.get_story_id_for_user()

        with self._db as _db:
            _db.insert(sql, [story_id, self._user_id, page_num, page_type, ])

    def get_story_id_for_user(self) -> any:
        sql = """SELECT id FROM story WHERE user_id = %s
                    AND submitted = 0"""
        with self._db as _db:
            result = _db.select_with_params(sql, [self._user_id, ])

        if result:
            return result[0][0]
        return None

    def save_document_path(self, story_id: str, file_path: str, page_num: str, page_type: str) -> any:
        sql = """INSERT INTO pages
                    (story_id, page_number, page_type, page_path)
                VALUES(%s, %s, %s, %s)"""
        file_path = file_path.replace('\\', '/')
        try:
            with self._db as _db:
                _db.insert(sql, [story_id, page_num, page_type, file_path, ])
            return True
        except Exception as e:
            return False

    def get_story_progress(self) -> any:
        sql = """SELECT
                    story_id,
                    last_page
                 FROM user_progress
                 WHERE user_id = %s
              """

        with self._db as _db:
            result = _db.select_with_params(sql, self._user_id)
        if result:
            story_id = result[0][0]
            last_page = result[0][1]

            content = self.get_page_content(story_id, last_page)
            image_path = self.get_image_path(story_id, last_page)
            return {
                'story_id': result[0][0],
                'last_page': result[0][1],
                'content': content,
                'image_path': image_path
            }
        else:
            return None

    def get_page_content(self, story_id: str, page_num: str) -> any:
        sql = """SELECT content FROM page_content
                WHERE story_id = %s 
                AND page_number = %s"""
        story_id = self.get_story_id_for_user()
        with self._db as _db:
            result = _db.select_with_params(sql, [story_id, page_num, ])
        if result:
            return result[0][0]
        else:
            return None

    def get_image_path(self, story_id: str, last_page: str) -> any:
        sql = """SELECT page_path from pages
                 WHERE story_id = %s
                 AND page_number = %s
                 AND page_type = 'image'"""
        with self._db as _db:
            result = _db.select_with_params(sql, [story_id, last_page, ])

        if result:
            return result[0][0]
        else:
            return None
