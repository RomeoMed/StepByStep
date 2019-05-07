import os
import logging
import json
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, \
    jsonify, session, abort, url_for, redirect, flash, send_from_directory
from flask_cors import CORS
from server import ServerHandler
from forms import *
from functools import wraps
from werkzeug.utils import secure_filename

#logPath = r'log\log.log'
# Set the name of the object we are logging for
#_logger = logging.getLogger("Boch_Log")
#_logger.setLevel(logging.DEBUG)
#handler = RotatingFileHandler(logPath, maxBytes=20971520, backupCount=10)
# Format the log message to display the time, object name, the logging level, and the message.
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#handler.setFormatter(formatter)
#_logger.addHandler(handler)

app = Flask(__name__)
_sh = ServerHandler()


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            form = LoginForm(request.form)
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def home():
    session.clear()
    if 'logged_in' in session:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm(request.form)
        return render_template('forms/login.html', form=form)
    else:
        user_name = request.form.get('name')
        password = request.form.get('password')

        valid = _sh.check_if_user_exists(user_name)

        if not valid:
            return redirect(url_for('register'))
        else:
            logged_in, message = _sh.login_user(user_name, password)
            if logged_in:
                session['logged_in'] = True
                session['user_email'] = user_name
                session['user_id'] = _sh.get_user_id(user_name)
                return redirect(url_for('landing'))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    _sh.logout(session['user_email'])
    session.clear()
    return redirect(url_for('home'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        form = RegisterForm(request.form)
        return render_template('forms/register.html', form=form)
    else:
        if not request.form.get('email') and not request.form.get('password'):
            return render_template('errors/400.html')

        user_obj = {
            "name": request.form.get('name'),
            "lastname": request.form.get('lname'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
            "address": request.form.get('address1'),
            "address2": request.form.get('address2'),
            "city": request.form.get('city'),
            "state": request.form.get('state'),
            "zip": request.form.get('zip'),
        }
        success, msg = _sh.create_user(user_obj)
        if not success:
            return render_template('errors/500.html')

        session['logged_in'] = True
        session['email'] = request.form.get('email')
        session['user_id'] = msg

        return redirect(url_for('security'))


@app.route('/security', methods=['POST', 'GET'])
@login_required
def security():
    if request.method == 'GET':
        result = _sh.get_security_questions()
        questions = [(q[0], q[1]) for q in result]
        form = SecurityQuestions(request.form)
        form.question1.choices = questions
        form.question2.choices = questions
        form.question3.choices = questions

        return render_template('forms/security_questions.html', form=form)
    else:
        user_email = session.get('user_email')
        question_obj = [
            [request.form.get('question1'), request.form.get('answer1')],
            [request.form.get('question2'), request.form.get('answer2')],
            [request.form.get('question3'), request.form.get('answer3')]
        ]

        _sh.store_security_questions(user_email, question_obj)

        return redirect(url_for('book_setup'))


@app.route('/check_new_user/<path:user>', methods=['POST'])
def check_new_user(user):
    exists = _sh.check_if_user_exists(user)
    if exists:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})


@app.route('/book-editor/setup', methods=['POST', 'GET'])
@login_required
def book_setup():
    if request.method == 'GET':
        form = BookSetup(request.form)
        return render_template('forms/book_setup.html', form=form)
    else:
        title = request.form.get('title')
        acknowledgement = request.form.get('acknowledgement') or ''
        page = 'acknowledgement'
        user_id = session['user_id']
        story_id = _sh.write_acknowledgement_page(title, acknowledgement, page, user_id)

        if story_id:
            session['story_id'] = story_id
            session['page_num'] = 1
            session['page_type'] = 'content'
            return redirect(url_for('book_writer'))


@app.route('/book-editor/writer', methods=['POST', 'GET'])
@login_required
def book_writer():
    if request.method == 'GET':
        form = BookWriter()
        if 'last_page' in session and 'content' in session:
            form.content.description = str(session['last_page'])
            form.content.data = session['content']
            session['page_num'] = session['last_page']
            del session['last_page']
            del session['content']
            session['update_existing'] = True

        form.content.description = str(session['page_num'])
        return render_template('/forms/book_content.html', form=form)


# @app.route("/intro", methods=['POST'])
# @login_required
# def intro():

#    return render_template('book_content.html')


@app.route('/landing', methods=['POST', 'GET'])
@login_required
def landing():
    if request.method == 'GET':
        return render_template('forms/login_landing.html')
    else:
        data = request.form.get('event')
        if data == 'continue':
            user_id = session['user_id']
            result = _sh.get_saved_progress(str(user_id))

            if result:
                session['content'] = result['content']
                session['story_id'] = result['story_id']
                session['last_page'] = result['last_page']

                return redirect(url_for('book_writer'))
            else:
                flash('no saved story found')
                return redirect(url_for('book_setup'))
        else:
            return redirect(url_for('book_setup'))


@app.route('/go_back', methods=['GET', 'POST'])
def go_back():
    session['last_page'] = str(session['page_num'] - 1)
    user_id = session['user_id']
    story_id = session['story_id']
    content = _sh.get_section(str(user_id), str(story_id), session['last_page'])

    if content:
        session['content'] = content

    return redirect(url_for('book_writer'))


@app.route('/advance', methods=['POST', 'GET'])
@login_required
def advance():
    page = str(session['page_num'])
    if 'upload' in request.files:
        file = request.files['upload']
        file_path = 'static/user_files/user_id_{}'.format(str(session['user_id']))
        fileName = secure_filename(file.filename)
        fileName = 'page_{}.image_{}'.format(str(session['page_num']), fileName)
        full_filepath = os.path.join(file_path, fileName)
        return_path = '/user_files/user_id_{}/{}'.format(str(session['user_id']), fileName)
        if os.path.exists(full_filepath):
            os.remove(full_filepath)
        file.save(os.path.join(file_path, fileName))
        _sh.save_image_path(return_path, str(session['user_id']), page)

        flash('file saved')
    story_text = request.form.get('content')
    success = _sh.write_page(story_text, page, str(session['user_id']))
    if success:
        session['page_num'] = int(session['page_num']) + 1
        if 'update_existing' in session:
            result = _sh.get_saved_progress(str(session['user_id']))

            if result:
                session['content'] = result['content']
            else:
                del session['update_existing']
        return redirect(url_for('book_writer'))
    else:
        flash('Error submitting request')


@app.route('/preview-book', methods=['GET'])
@login_required
def preview():
    preview_obj = _sh.get_book_preview(str(session['story_id']), str(session['story_id']))
    return render_template('forms/book_preview.html', result=preview_obj)


@app.route('/forgot')
def forgot():
    return render_template('/forms/forgot.html')


@app.route('/uploads/<path:filename>')
def stored_file(filename):
    media_folder = 'user_files'
    filename = filename[filename.index('/'):]
    return send_from_directory(media_folder, filename, as_attachment=True)


if __name__ == '__main__':
    app.secret_key = 'f3cfe9ed8fae309f02079dbf'
   # _logger.info('Server is Listening.....')
    app.run(debug=True)
