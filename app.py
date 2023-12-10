import json
import secrets  # Import the secrets module
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Used for flashing messages

# Load user data from a JSON file
try:
    with open('user_data.json', 'r') as file:
        user_data = json.load(file)
except FileNotFoundError:
    user_data = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        entered_username = request.form['username']
        entered_password = request.form['password']

        if entered_username in user_data and user_data[entered_username]['password'] == entered_password:
            return redirect(url_for('success', username=entered_username))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']

        # Check username length
        if len(new_username) > 12:
            flash('Username cannot be longer than 12 characters', 'error')
        # Check if username already exists
        elif new_username in user_data:
            flash('Username already exists', 'error')
        # Check password length
        elif len(new_password) < 6:
            flash('Password must be at least 6 characters long', 'error')
        else:
            # Generate a random key using secrets module
            new_key = secrets.token_urlsafe(16)  # 16 bytes gives a 24-character key
            # Add the new user to the dictionary with the generated key
            user_data[new_username] = {'password': new_password, 'key': new_key}

            # Save the updated user data to the JSON file
            with open('user_data.json', 'w') as file:
                json.dump(user_data, file, indent=2)

            flash('Signup successful! You can now log in.', 'success')
            return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/success/<username>')
def success(username):
    return render_template('account_management.html', username=username, key=user_data[username]['key'])

if __name__ == '__main__':
    app.run(debug=True)
