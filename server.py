import psycopg2
import requests
from flask import Flask, render_template, request, redirect, make_response, session, flash, url_for
import os
from flask_bcrypt import Bcrypt
from models.db import sql_select, sql_write, sql_select_one
import time


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = os.environ.get('secret_session')



# main page reaches themealdb API for random recipe 
# unpacks API call and checks if ingredients length is under 800
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


# sign up page with form for sign up 
@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

#signup form action, creates password hash, writes userdata and hash
# into database 
@app.route('/sign_up_action', methods=['POST', 'GET'])
def sign_up_action():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    pw_hash = bcrypt.generate_password_hash(password).decode('utf8')
    sql_write('INSERT INTO users(username,email,pw_hash) VALUES(%s,%s,%s)', [username,email,pw_hash])
    flash('Your account has been created! You can now login')
    return redirect(url_for('sign_in'))
# sign in page 
@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

# sign in method - checks if user already exists in database
# checks if user exists in db, then checks pw hash, if both conditionals pass session is set and user logged in
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
        



# signs user out of program by removing session key 
@app.route('/sign_out')
def sign_out():
    session.pop('username')
    flash('Sucessfully logged out')
    return redirect('/')# 


#retrives recipe form data and inserts comment into comments 
# database including id, comment, title, image url 
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


# selects results from comments data base and sends list as variable to page for scrolling feed type view ordered by most recent 
@app.route('/feed')
def feed():
    username = session.get('username')
    ids = sql_select('SELECT id FROM users WHERE username=%s',[username])
    id = ids[0]
    results = sql_select('SELECT id, username, recipe_name, comment, image_url, post_id FROM users JOIN comment ON users.id = comment.user_id ORDER BY post_id DESC',[id])
    # print(results)

    for list in results:
        list = list 
    print(f'list results is {results}')
    
    return render_template('feed.html', results=results, username=username)

# Guest account login, checks if guest already registered in db, creates and account, then signs in 
@app.route('/guest_sign_in')
def guest_sign_in():
    session['username']='GuestAccount'
    acc = sql_select_one('SELECT username FROM users WHERE username = %s',['GuestAccount'])
    print(f'account name is {acc[0]}')
    if acc[0] is not acc[0]: 
        sql_write('INSERT INTO users(username) VALUES(%s)', ['GuestAccount'])
    else:
        pass
    flash('logged as a GuestAccount')
    return redirect ('/')

#profile page wich displays all posts made by the logged in users, and gives
# option to delete/update posts

@app.route('/profile')
def profile():
    username = session.get('username')
    id = sql_select_one('SELECT id FROM users WHERE username=%s',[username])
    print(id[0])
    results = sql_select('SELECT id, username, recipe_name, comment, image_url, post_id FROM users INNER JOIN comment on user_id = %s WHERE id=%s ORDER BY post_id DESC  ',[id[0],id[0]])
    print(results)
    return render_template('profile.html', results=results, username=username)

#delete action - deletes row from database by matching post_id from delete form
@app.route('/delete', methods=['POST', 'GET'])
def delete():
    post_id = request.form.get('post_id')
    print(f'the post id is...{post_id}')
    sql_write('DELETE FROM comment WHERE post_id = %s', [post_id])
    return redirect('/profile')

if __name__ == '__main__':
    from dotenv import load_dotenv
    app.run(port=5019, debug=True)