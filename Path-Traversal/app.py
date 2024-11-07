from flask import *
from urllib.parse import unquote
import os
import logging

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_FILE = os.path.join(ROOT_DIR, "instance/access.log")
ENABLE_SAFETY = False

app = Flask(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)

@app.route('/')
def index():
    files = os.listdir(os.path.join(ROOT_DIR, "files"))
    return render_template('index.html', files=files)


@app.post("/upload")
def upload():
    file = request.files.get('file')
    if file:
        filename = request.form.get('filename')
        file_path = os.path.join(ROOT_DIR, "files", (filename.replace("../", "") or file.filename) if ENABLE_SAFETY else file.filename)
        file.save(file_path)
        return redirect(url_for("index"))
    return redirect(url_for("index"))


@app.get('/download')
def download():
    file_path = request.args.get('file')
    if file_path:
        if ENABLE_SAFETY:
            sanitized = unquote(file_path).replace("../", "")
            sanitized_check = sanitized.lower()
            if "app" in sanitized_check or "docker" in sanitized_check or "aes" in sanitized_check:
                return redirect(url_for("index"))
        return send_file(os.path.join(ROOT_DIR, "files", sanitized if ENABLE_SAFETY else file_path), as_attachment=True)
    return redirect(url_for("index"))


@app.route("/admin")
def admin():
    return jsonify({"403": "Forbidden"})

if __name__ == '__main__':
    app.run(host="0.0.0.0")
