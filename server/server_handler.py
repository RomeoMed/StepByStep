from db import Database
from typing import Optional
from encryption import AESCipher
from pdf import PdfHandler
from story import Story
from user import User


class ServerHandler:
    def __init__(self):
        self._db = Database()

    def get_user_id(self, email: str) -> Optional[str]:
        user = User(email)
        return user.get_user_id()

    def login_user(self, email: str, password: str) -> any:
        user = User(email)
        return user.login(password)

    def logout(self, email: str) -> None:
        user = User(email)
        user.logout()

    def get_security_questions(self):
        sql = "SELECT * FROM questions"

        with self._db as _db:
            result = _db.select(sql)

        return result if result else None

    def create_user(self, user_obj: dict) -> any:
        email = user_obj.get('email')
        user = User(email)
        return user.create_new_user(user_obj)

    def check_if_user_exists(self, email: str) -> bool:
        user = User(email)
        return user.exists_user()

    def store_security_questions(self, user_email: str, question_obj: any) -> None:
        user = User(user_email)
        user.insert_security_questions(question_obj)

    def write_acknowledgement_page(self, title: str, acknowledgement: str, page: str, user_id: str):
        story = Story(user_id)
        story_id = story.create_new_story(title)

        page_name = 'page_{}'.format(page)
        pdf_writer = PdfHandler(page_name, user_id)
        pdf_writer.set_document_title('Acknowledgement')
        file_path = pdf_writer.write_document(acknowledgement)
        page_num = 0

        return story.save_document_path(str(story_id), file_path, str(page_num), 'acknowledgement')

    def write_page(self, text: str, page: str, user_id: str) -> any:
        story = Story(user_id)

        page_name = 'page_{}'.format(page)
        pdf_writer = PdfHandler(page_name, user_id)

        story_id = story.get_story_id_for_user()

        filepath = pdf_writer.write_document(text)
        story.save_progress(story_id, page, 'body')
        story.save_document_path(story_id, filepath, page, 'text')

        return True

    def get_saved_progress(self, user_id: str) -> any:
        story = Story(user_id)

        return story.get_story_progress()

    def save_image_path(self, fullpath: str, user_id: str, page_num: str) -> None:
        story = Story(user_id)
        story_id = story.get_story_id_for_user()

        story.save_document_path(story_id, fullpath, page_num, 'image')

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