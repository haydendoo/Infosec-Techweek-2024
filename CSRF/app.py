from flask import Flask, render_template, request, make_response, redirect
from flask_cors import CORS
import secrets

app = Flask(__name__)
CORS(app, supports_credentials=True)

# A "Database" containing the users
users = {
    "admin": {
        "password": "password123",
        "token": secrets.token_urlsafe(32)
    }
}

@app.route('/')
def index():
    user = request.cookies.get("user")
    token = request.cookies.get("token")
    if user == "admin" and token == users['admin']['token']:
        return render_template('index.html', admin=True)
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username not in users or password != users[username]['password']:
            return render_template('login.html', invalid=True)

        res = make_response(redirect('/'))
        res.set_cookie('user', username, samesite='None', secure=True)
        res.set_cookie('token', users[username]['token'], samesite='None', secure=True)

        return res
    
    return render_template('login.html')

@app.route('/changepassword', methods=['POST', 'GET'])
def changepassword():
    user = request.cookies.get("user")
    token = request.cookies.get("token")

    if user not in users or token != users[user]['token']:
        return render_template('changepassword.html', invalid=True)

    if request.method == "POST":
        password = request.form.get("password")
        users[user]['password'] = password
        return redirect('/')

    return render_template('changepassword.html')

if __name__ == "__main__":
    app.run(port=5000, debug=True)