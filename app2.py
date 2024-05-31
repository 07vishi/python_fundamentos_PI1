from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Predefined credentials (for demonstration purposes)
VALID_USERNAME = 'admin'
VALID_PASSWORD = 'password123'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        flash('Login successful!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Invalid username or password.', 'danger')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)