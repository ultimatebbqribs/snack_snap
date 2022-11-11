import psycopg2
import requests
from flask import Flask, render_template, request, redirect, make_response, session, flash, url_for
import os
from flask_bcrypt import Bcrypt
from models.db import sql_select, sql_write
import time

OMDB_API_KEY = os.environ.get('omdb_key')


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = '534b6f3f5144a551644226ec2bca9f6ddcbb977730be7ac5f1737325412ec8ea'

@app.route('/')
@app.route('/main')
def main():
    username = session.get('username')
    mealsdb_api = requests.get('https://www.themealdb.com/api/json/v1/1/random.php')
    recipe = mealsdb_api.json()
    indredients = []
    for dict in recipe['meals']:
        meals = dict 
    print(meals)
    print(meals['strIngredient1'])
    image = meals['strMealThumb']
    title = meals['strMeal']
    instructions= meals['strInstructions']
    if len(instructions) < 800:
        return render_template('main.html', username=username, image=image, title=title, instructions=instructions)
    else:
        # time.sleep(.1)
        return main()



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
        




@app.route('/sign_out')
def sign_out():
    session.pop('username')
    flash('Sucessfully logged out')
    return redirect('/')

@app.route('/recipe_comment', methods=['POST','GET'])
def recipe_comment():
    title = request.form.get('title')
    comment = request.form.get('comment')
    image = request.form.get('image')
    username = session.get('username')
    print(username)
    ids = sql_select('SELECT id FROM users WHERE username=%s',[username])
    id = ids[0]

    print(f'form value for recipe is {title}')

    sql_write('INSERT INTO comment (user_id, comment, recipe_name, image_url) VALUES (%s, %s, %s, %s)', [id, comment, title, image])


    flash(f'Comment "{comment}" added to database by {username}')
    return redirect ('/')

@app.route('/<username>')
def profile(username):

    return render_template ('profile.html')

@app.route('/feed')
def feed():
    username = session.get('username')
    ids = sql_select('SELECT id FROM users WHERE username=%s',[username])
    id = ids[0]
    results = sql_select('SELECT id, username, recipe_name, comment, image_url FROM users INNER JOIN comment on user_id = %s',[id])
    # print(results)

    for list in results:
        list = list 
    print(f'list results is {results}')
    
    return render_template('feed.html', results=results)

if __name__ == '__main__':
    from dotenv import load_dotenv
    app.run(port=5019, debug=True)