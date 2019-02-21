from flask import Flask, request, send_from_directory
from datetime import datetime
# set the project root directory as the static folder, you can set others.app = Flask(__name__, static_url_path='')
import os

# credits to https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask

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
    <p>{file_paths}</p>
    
    <img src="http://loremflickr.com/600/400" />
    """.format(time=the_time, file_paths=file_paths)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('.', path)
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

