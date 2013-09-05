import os
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        error = validate_login(request.form['user'],
                               request.form['password'])
        if not error:
            return redirect(url_for('download'))
    return render_template('login.html', error=error)


@app.route('/download', methods=['GET', 'POST'])
def download():
    return render_template('download.html')


def validate_login(user, password):
    result = []
    if len(user) != 6:
        result.append('Username has to be 6 characters')
    if len(password) <= 6 or len(password) >= 12:
        result.append(
            'Password needs to be at least 6 not more than 12 characters long')
    return ', '.join(result)


def run_server():
    app.run(debug=True)
