from flask import Flask, render_template, request, redirect, url_for, session
from backend import authenticate, generate_unique_portfolios
import os, json

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Must be set for sessions

USERS_FILE = "users.json"

# Load users from file (or create if not present)
def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_user(username, password):
    users = load_users()
    users[username] = password
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            return render_template('register.html', error="Username already exists.")
        save_user(username, password)
        session['user'] = username
        return redirect('/')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    users = load_users()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['user'] = username
            return redirect('/')
        return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    if 'user' not in session:
        return redirect('/login')
    investment = float(request.form['investment'])
    risk_level = request.form['risk']
    time_goal = request.form['goal']
    token = authenticate()
    portfolios = generate_unique_portfolios(token, investment, risk_level, time_goal)
    return render_template('results.html', portfolios=portfolios)

if __name__ == '__main__':
    app.run(debug=True)
