# app/routes.py

from flask import render_template, request, redirect, url_for, flash, session, send_file
from werkzeug.utils import secure_filename
import os
import bcrypt
import pandas as pd
from .utils import extract_information, convert_to_wav, audio_file_to_text, save_to_excel

# Function to register routes with the Flask app
def register_routes(app, mongo):
    @app.route('/')
    def root():
        return redirect(url_for('signup'))

    @app.route('/index')
    def index():
        if 'username' in session:
            return render_template('index.html')
        else:
            return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            # Check if the user exists in the database
            user = mongo.db.users.find_one({"username": username})

            # Verify the password
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                session['username'] = username
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password', 'danger')

        return render_template('login.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Check if the username already exists
            if mongo.db.users.find_one({"username": username}):
                flash('Username already exists', 'danger')
            else:
                # Insert new user into the database
                mongo.db.users.insert_one({"username": username, "password": hashed_password})
                flash('Signup successful! Please log in.', 'success')
                return redirect(url_for('login'))

        return render_template('signup.html')

    @app.route('/upload', methods=['POST'])
    def upload():
        if 'username' not in session:
            return redirect(url_for('login'))

        if 'files' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files')
        data = []

        for file in files:
            if file.filename.endswith(".mp4"):
                filename = secure_filename(file.filename)
                file_path = os.path.join("uploads", filename)
                file.save(file_path)
                wav_file_path = convert_to_wav(file_path)
                text = audio_file_to_text(wav_file_path)
                if text:
                    extracted_data = extract_information(text)
                    if extracted_data:
                        data.extend(extracted_data)
                os.remove(wav_file_path)
                os.remove(file_path)
            else:
                flash(f"Unsupported file format: {file.filename}")

        if data:
            save_to_excel(data)
            flash('Data successfully processed and saved to Excel file.', 'success')
        else:
            flash('No data to save to Excel.', 'warning')

        return redirect(url_for('index'))

    @app.route('/view')
    def view():
        if 'username' not in session:
            return redirect(url_for('login'))

        if os.path.exists("sample_file.xlsx"):
            df = pd.read_excel("sample_file.xlsx")
            df.columns = [col.replace(' ', '') for col in df.columns]
            return render_template('view.html', tables=df.to_dict(orient='records'))
        else:
            flash('No Excel file found.', 'warning')
            return redirect(url_for('index'))

    @app.route('/download')
    def download():
        if 'username' not in session:
            return redirect(url_for('login'))

        file_path = os.path.join(os.getcwd(), 'sample_file.xlsx')  # Adjust this path accordingly

        if os.path.exists(file_path):
            try:
                return send_file(file_path, as_attachment=True)
            except Exception as e:
                flash(f'Error downloading file: {str(e)}', 'danger')
                return redirect(url_for('index'))
        else:
            flash('No Excel file found.', 'warning')
            return redirect(url_for('index'))

    @app.route('/logout')
    def logout():
        session.pop('username', None)
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))
