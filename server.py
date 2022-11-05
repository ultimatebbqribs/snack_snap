import psycopg2
from flask import Flask, render_template, request, redirect, make_response, session
import cloudinary
import cloudinary.uploader
import os
from flask_bcrypt import Bcrypt
from models.db import sql_select, sql_write

cloud_name = os.environ.get('cloud_name')
COLOUDINARY_API_KEY = os.environ.get('api_key')
COLOUDINARY_API_SECRET = os.environ.get('api_secret')

cloudinary.config( 
  cloud_name = cloud_name,
  api_key = COLOUDINARY_API_KEY, 
  api_secret = COLOUDINARY_API_SECRET, 
)

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/sign_up_action', methods=['POST', 'GET'])
def sign_up_action():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    pw_hash = bcrypt.generate_password_hash(password).decode('utf8')
    sql_write('INSERT INTO users(username,email,pw_hash) VALUES(%s,%s,%s)', [username,email,pw_hash])
    return redirect('/')

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/sign_in_action',methods=['POST', 'GET'])
def sign_in_action():
    email = request.form.get('email')
    password = request.form.get('password')
    results = sql_select('SELECT email, pw_hash FROM users WHERE email = %s', [str(email)])
    for row in results:
        db_email, pw_hash = row
    print(db_email, pw_hash)
    if bcrypt.check_password_hash(pw_hash, password):
        print(f'successful login')
    else:
        (f'username or password incorrect')


    return redirect('/')

@app.route('/add_post', methods=['POST', 'GET'])
def add_post():


    return render_template('/add_post.html')

@app.route('/img_upload', methods=['POST', 'GET'])
def img_upload():
    #get the image from post req
    image = request.files['image']

    #upload the image 
    response = cloudinary.uploader.upload(image, filenme=image.filename)
    print(response)

    #get the file name
    image_id = image.filename


if __name__ == '__main__':
    from dotenv import load_dotenv
    app.run(port=5014, debug=True)