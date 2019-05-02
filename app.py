from flask import Flask, request, send_from_directory
from datetime import datetime
import os
import sys
from pprint import pformat
# credits to https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
import subprocess

# set the project root directory as the static folder, you can set others
app = Flask(__name__, static_url_path='')

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")
    file_paths = []
    for root, dirs, files in os.walk("."):
        file_paths += [os.path.join(root, dir_) for dir_ in dirs]
        file_paths += [os.path.join(root, file_) for file_ in files]
    file_paths = "<br />".join(file_paths)
    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>
    <p>pwd {pwd}.</p>
    <p>The env: {environ}.</p>
    <h3>files in .:</h3>
    <p>{file_paths}</p>
    
    <img src="http://loremflickr.com/600/400" />
    """.format(time=the_time, file_paths=file_paths, pwd=os.path.abspath("."), environ=pformat(dict(os.environ)))

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('.', path)

@app.route('/compile')
def compile():
    text = "OK."
    try:
        output = subprocess.run(["/app/TeXLive/bin/x86_64-linux/xelatex", "--shell-escape", "-synctex=1",
                                 "-interaction=nonstopmode", "/app/TeXLive/bin/x86_64-linux/test.tex"],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=None)
        text += "\nReturn code: %s\n" % output.returncode
        text += output.stdout.decode()
    except Exception as e:
        text = "type: %s, error: %s" % (type(e), e)
    return text

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

