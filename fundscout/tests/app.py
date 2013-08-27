import os
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        error = 'Invalid username'
    return render_template('login.html', error=error)


def run_server():
    app.run(debug=True)
