from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
import smtplib
import numpy as np
from PIL import Image, ImageOps
import webbrowser
from rest_framework.decorators import api_view
from django.core import exceptions, validators
from rest_framework.response import Response
import requests
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


@app.post('/predict')
def predict(input_parameters : model_input):
 test = []
 #real_image = Image.open('/content/drive/MyDrive/Fear.jpg') #store image in temp var to be accessed as such to store in folder
 #image = cv2.imread('/content/drive/MyDrive/Fear.jpg')
 #files = sys.argv[1]
 input_data = input_parameters.json()
 input_dictionary = json.loads(input_data)
 the_url = input_dictionary['str1']
 real_image = Image.open(the_url)
 image = cv2.imread(the_url)
 image = cv2.resize(image, (150,150))
 test.append(image)
 test = np.array(test, dtype='float32')
 test = np.expand_dims(test, axis=1)
 test_image = test[0]
 model = tf.keras.models.load_model('/content/drive/MyDrive/Datasets/keras_model.h5')
 prediction = model.predict(test_image)
 if ((prediction[0][3] > prediction[0][0]) & (prediction[0][3] > prediction[0][1]) & (prediction[0][3] > prediction[0][2])):
        real_image.save(f'/content/drive/MyDrive/Datasets/Train/Sad/Sad{str(datetime.now())}.jpg', 'JPEG')
        return('Sad')
 elif ((prediction[0][2] > prediction[0][0]) & (prediction[0][2] > prediction[0][1]) & (prediction[0][2] > prediction[0][3])):
        real_image.save(f'/content/drive/MyDrive/Datasets/Train/Happy/Happy{str(datetime.now())}.jpg', 'JPEG')
        return('Happy')
 elif ((prediction[0][1] > prediction[0][0]) & (prediction[0][1] > prediction[0][2]) & (prediction[0][1] > prediction[0][3])):
        real_image.save(f'/content/drive/MyDrive/Datasets/Train/Fear/Fear{str(datetime.now())}.jpg', 'JPEG')
        return('Fear')
 elif ((prediction[0][0] > prediction[0][1]) & (prediction[0][0] > prediction[0][2]) & (prediction[0][0] > prediction[0][3])):
      real_image.save(f'/content/drive/MyDrive/Datasets/Train/Angry/Angry{str(datetime.now())}.jpg', 'JPEG')
      return('Angry')
 else:
   return('Null')
                      
                
    
    
 





    
