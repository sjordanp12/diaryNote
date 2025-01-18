from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
from datetime import datetime
from bson import ObjectId


app = Flask(__name__)

load_dotenv()
# Mengambil MONGO_URI dari variabel lingkungan
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

app.secret_key = 'supersecretkey'  # Ganti dengan key yang lebih aman

mongo = PyMongo(app)
bcrypt = Bcrypt(app)  # Inisialisasi Flask-Bcrypt

# Halaman utama - menampilkan catatan pengguna
@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Menampilkan catatan berdasarkan username
    user_notes = mongo.db.notes.find({"username": session['username']})
    return render_template('home.html', notes=user_notes)

# Halaman login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Cek apakah user ada di database
        user = mongo.db.users.find_one({"username": username})

        # Menggunakan bcrypt untuk memeriksa hash password
        if user and bcrypt.check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

# Halaman logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Halaman registrasi
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash password menggunakan bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        existing_user = mongo.db.users.find_one({"username": username})

        if existing_user:
            flash("Username already exists!")
        else:
            # Simpan user dengan password yang telah di-hash
            mongo.db.users.insert_one({"username": username, "password": hashed_password})
            flash("Registration successful! You can log in now.")
            return redirect(url_for('login'))

    return render_template('register.html')

# Halaman untuk menambah catatan
@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        mongo.db.notes.insert_one({
            "username": session['username'],
            "title": title,
            "content": content,
            "created_at": current_time
        })
        return redirect(url_for('home'))

    return render_template('add_note.html')
@app.route('/delete_note/<note_id>', methods=['POST'])
def delete_note(note_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    # Menghapus catatan berdasarkan ID
    mongo.db.notes.delete_one({"_id": ObjectId(note_id)})
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
