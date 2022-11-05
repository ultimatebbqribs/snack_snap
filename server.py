import psycopg2
from flask import Flask, render_template, request, redirect, make_response, session
import cloudinary
import cloudinary.uploader
import os

cloud_name = os.environ.get('cloud_name')
COLOUDINARY_API_KEY = os.environ.get('api_key')
COLOUDINARY_API_SECRET = os.environ.get('api_secret')

cloudinary.config( 
  cloud_name = cloud_name,
  api_key = COLOUDINARY_API_KEY, 
  api_secret = COLOUDINARY_API_SECRET, 
)

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

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
    app.run(port=5011, debug=True)