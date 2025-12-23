from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
import os
from backend import authenticate, generate_unique_portfolios, generate_pie_chart

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Store users (in production, use a database)
USERS = {}

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USERS and USERS[username] == password:
            session['user'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USERS:
            return render_template('register.html', error='User already exists')
        
        USERS[username] = password
        session['user'] = username
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/results', methods=['POST'])
def results():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    investment = float(request.form['investment'])
    risk = request.form['risk']
    goal = request.form['goal']
    
    token = session['user']
    portfolios = generate_unique_portfolios(token, investment, risk, goal)
    
    for i, portfolio in enumerate(portfolios):
        chart_filename = f'portfolio_{i+1}.png'
        portfolio['chartfilename'] = chart_filename
    
    return render_template('results.html', portfolios=portfolios)

if __name__ == '__main__':
    app.run(debug=True)
