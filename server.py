import psycopg2
import requests
from flask import Flask, render_template, request, redirect, make_response, session, flash, url_for
import os
from flask_bcrypt import Bcrypt
from models.db import sql_select, sql_write

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
        
@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/search_results', methods=['GET'])
def search_results():
    movie=request.args['movie']
    movie_api = requests.get(f'https://www.omdbapi.com/?s={movie}&apikey=a0b50029')
    r = movie_api.json()
    search = r['Search']
    print(movie)

    return render_template('search_results.html', search=search)

@app.route('/sign_out')
def sign_out():
    session.pop('username')
    flash('Sucessfully logged out')
    return redirect('/')

if __name__ == '__main__':
    from dotenv import load_dotenv
    app.run(port=5019, debug=True)