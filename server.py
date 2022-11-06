import psycopg2
import requests
from flask import Flask, render_template, request, redirect, make_response, session, flash, url_for
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
app.config['SECRET_KEY'] = '534b6f3f5144a551644226ec2bca9f6ddcbb977730be7ac5f1737325412ec8ea'

@app.route('/')
@app.route('/main')
def main():
    username = session.get('username')
    mealsdb_api = requests.get('https://www.themealdb.com/api/json/v1/1/random.php')
    recipe = mealsdb_api.json()
    for dict in recipe['meals']:
        meals = dict 
    image = meals['strMealThumb']
    title = meals['strMeal']
    instructions= meals['strInstructions']
    if len(instructions) > 900:
        mealsdb_api = requests.get('https://www.themealdb.com/api/json/v1/1/random.php')
    else:
        pass

    return render_template('main.html', username=username, image=image, title=title, instructions=instructions)


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
    flash('Your account has been created! You can now login')
    return redirect(url_for('sign_in'))

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/sign_in_action',methods=['POST', 'GET'])
def sign_in_action():
    email = request.form.get('email')
    password = request.form.get('password')
    if sql_select('SELECT email, pw_hash FROM users WHERE EXISTS (SELECT 1 from users WHERE email = %s)', [str(email)]):
        results = sql_select('SELECT username, email, pw_hash FROM users WHERE email = %s', [str(email)])
        print(f'SQL RESULTS ARE .... {results}')
        for row in results:
            username, db_email, pw_hash = row
        if bcrypt.check_password_hash(pw_hash, password):
            flash(f'Successful login')
            session['username']=username
            return redirect('/')
        else:
            
            flash(f'email or password incorrect')
            return redirect('/sign_in')
    else:
        flash(f'email or password incorrect')
        return redirect('/sign_in')
        

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

@app.route('/sign_out')
def sign_out():
    session.pop('username')
    flash('Sucessfully logged out')
    return redirect('/')

if __name__ == '__main__':
    from dotenv import load_dotenv
    app.run(port=5015, debug=True)