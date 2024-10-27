from flask import Flask, redirect, url_for, render_template, request,send_from_directory,jsonify
import os
import keras
from tensorflow.keras.utils import img_to_array
import numpy as np
import cv2 as cv
from flask import send_from_directory
from werkzeug.utils import secure_filename
import PIL
import google.generativeai as genai
from decouple import config
import requests

# Access the API key securely (replace with your method)
# API_KEY = config('GOOGLE_API_KEY') 
app=Flask(__name__)

genai.configure(api_key="AIzaSyDniZ7Kvj4T4uRUWlW93GlRW7qgTvHi64g")

# Define the folder where uploaded images will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def save_image_and_return_path(img):
    filename = secure_filename(img.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img.save(filepath)
    return filename, filepath

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# def detection_img(img_url):
#     url = "https://api.langchain.com/genai/v1/model/gemini-pro-vision"
    
#     prompt = """
#     Tell about the cracked detection and highlights percentage also of given image that how much particular images are cracked and identify the cracked image or non crack images also. Apart from this don't say anything else.
#     """

#     payload = {
#         "prompt": prompt,
#         "inputs": {
#             "image_url": img_url
#         }
#     }

#     API_KEY = config('GOOGLE_API_KEY') 

#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json"
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     if response.status_code == 200:
#         print(response)
#         return response.json()['result']
#     else:
#         print(f"Error: {response.status_code} - {response.text}")
#         return f"Error: {response.status_code} - {response.text}"

def detection_img(img):
#  Your journey to a healthier heart starts now."""
    prompt="""
    Tell about the cracked detection and highlights percentage also of given image that how much particular images are cracked and identify the cracked image or non crack images also. Apart from this don't say anything else.
    """
    model = genai.GenerativeModel('gemini-pro-vision')
    img = PIL.Image.open(img)

    response = model.generate_content([prompt,img])
    return response.text

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    img_path = None
    if request.method == 'POST':
        location = request.form.get('location')
        img = request.files['img']

        if img.filename != '':
            try:
                result = detection_img(img)
                if result is not None:
                    response=result
                else:
                    print("Failed to detect image")
                ## image saving 
                return render_template('index.html', location=location, img=img, img_path=img_path, result=response)#,pred_val=pred_val)
            except Exception as e:
                # Handle the exception gracefully, you can log the error for debugging
                print("Error occurred:", e)
                return render_template('index.html')  # Render an error page to inform the user
        else:
            # Handle the case where img is not defined or invalid
            return render_template('index.html', message="Invalid image")
    else:
        return render_template('index.html')



if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0")