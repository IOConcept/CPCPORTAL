from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

if not os.path.exists('CPCCOMMS.json'):
    with open('CPCCOMMS.json', 'w') as f:
        json.dump([], f)

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
            print('Form submitted!')
            table_id = request.form['table_id']
            pending_data = {
                'table_id': table_id,
                'created_by': session['username']
            }
            with open('pending.json', 'w') as f:
                json.dump(pending_data, f)
            return redirect(url_for('table'))
        return render_template('dashboard.html', username=session['username'], tables=tables)
    else:
        return redirect(url_for('login'))


@app.route('/save_pending', methods=['POST'])
def save_pending():
    if 'username' in session:
        pending_data = request.get_json()
        with open('pending.json', 'w') as f:
            json.dump(pending_data, f)
        return jsonify(success=True)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
