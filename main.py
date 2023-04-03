from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

with open('CPCCOMMS.json') as f:
    data = json.load(f)


@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/dashboard', methods=['POST'])
def dashboard():
    username = request.form['username']
    password = request.form['password']

    for entry in data:
        if f"%{username.upper()}%{password}%" == entry['message']:
            session['username'] = username
            return redirect(url_for('table'))

    return render_template('login.html', error='Invalid username or password')


@app.route('/table', methods=['GET', 'POST'])
def table():
    if 'username' in session:
        tables = [entry['message'].split('%')[-2] for entry in data if 'ESTABLISH CPC TABLE' in entry['message']]
        if request.method == 'POST':
            table_id = request.form['table_id']
            message = f"%{session['username'].upper()}%PP%C0%T{table_id}%100%CREATE CPC TABLE {table_id}%"
            data.append({'time': 'Now', 'message': message, 'response': ''})
            with open('CPCCOMMS.json', 'w') as f:
                json.dump(data, f, indent=4)
            return redirect(url_for('table'))
        return render_template('dashboard.html', username=session['username'], tables=tables)
    else:
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
