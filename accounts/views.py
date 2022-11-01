from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from rest_framework.decorators import api_view
from django.core import exceptions, validators
from rest_framework.response import Response
import smtplib
import requests
import json
from github import Github
import os
import os.path
import base64
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageOps
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
g = Github("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")
repo = g.get_repo("RohaanJohn/DhwaniAPI")
# Create your views here.

def login(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            #return render(request,'login.html')
            messages.info(request, 'invalid credentials')
            return render(request,'login.html')

    else:
        return render(request,'login.html')
        
        

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return redirect('register')
            else:
              user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
              user.save();
              print('User created')
              return redirect('login')
        else:
            messages.info(request,'Password not matching')
            return redirect('register')
        return redirect('/')

    else:
    
       return render(request,'register.html')
def logout(request):
    auth.logout(request)
    return redirect('/')

def contact(request):
    
      
  if request.method== 'POST':
        email = request.POST['email']
        username = request.POST['username']
        msg = request.POST['message']

        s = smtplib.SMTP('smtp.gmail.com', 587) 
        s.starttls() 
        s.login("rohaanrenujohn.b20cs1154@mbcet.ac.in", "rohaanrenujohn123")
        SUBJECT = "Travello"
        TEXT = f"Hi {username}! We will look into your message and send you a reply as soon as possible if needed. Thank you for using Travello!"
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        s.sendmail("rohaanrenujohn.b20cs1154@mbcet.ac.in", f"{email}", message)

        s = smtplib.SMTP('smtp.gmail.com', 587) 
        s.starttls() 
        s.login("rohaanrenujohn.b20cs1154@mbcet.ac.in", "rohaanrenujohn123")
        SUBJECT = "Contact"
        TEXT = f"Using the email address {email}, here is a message from {username}: {msg}"
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        s.sendmail("rohaanrenujohn.b20cs1154@mbcet.ac.in", "rohaanrenujohn.b20cs1154@mbcet.ac.in", message)

        s.quit()
        

      
        return redirect('/')
  else:
        return render(request,'contact.html')


@api_view(['GET', 'POST'])
def predict(request):
                
              if request.method== 'POST':
                    img = request.FILES['img']
                    test = []
                    final_image = Image.open(img)
                    temp_image = final_image 
                    buf = BytesIO()
                    temp_image.save(buf, 'jpeg')
                    buf.seek(0)
                    image_bytes = buf.read()
                    buf.close()
                    string = base64.b64encode(image_bytes)
                    pic_url = f'FinalImage/Image{str(datetime.now())}.jpg'
                    repo.create_file(pic_url, "commit", base64.b64decode(string))
                    url = 'http://869b-34-138-189-235.ngrok.io/predict'
                    input_data_for_model = {
                      'str1' : pic_url
                    }
                    input_json  = json.dumps(input_data_for_model)
                    result = requests.post(url, data=input_json)
                    the_output = result.text
                    the_result = the_output.replace('"','')
                    return Response({"output":the_result})
                       
              else:
                return render(request,'emotionanalysis.html')
   # [(0 is Happy), (1 is Angry), (2 is Sad), (3 is Fear)]


                      
                
    
    
 





    
