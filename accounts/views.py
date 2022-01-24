from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
import smtplib

import pandas as pd

#from IPython.display import display, Javascript
#from base64 import b64decode
import tensorflow.keras
from PIL import Image, ImageOps

import webbrowser
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
            messages.info(request, 'invalid credentials')

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
        s.login("thealphadebuggers@gmail.com", "alphadebuggers12345689")
        SUBJECT = "Travello"
        TEXT = f"Hi {username}! We will look into your message and send you a reply as soon as possible if needed. Thank you for using Travello!"
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        s.sendmail("thealphadebuggers@gmail.com", f"{email}", message)

        s = smtplib.SMTP('smtp.gmail.com', 587) 
        s.starttls() 
        s.login("thealphadebuggers@gmail.com", "alphadebuggers12345689")
        SUBJECT = "Contact"
        TEXT = f"Using the email address {email}, here is a message from {username}: {msg}"
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        s.sendmail("thealphadebuggers@gmail.com", "thealphadebuggers@gmail.com", message)

        s.quit()
        

      
        return redirect('/')
  else:
        return render(request,'contact.html')
        
def trashdetection(request):
                
                    
                    
                
                    # Disable scientific notation for clarity
                    pd.set_printoptions(suppress=True)

                    # Load the model
                    model = tensorflow.keras.models.load_model('C:\\Users\\acer\\Downloads\\keras_model (1).h5')

                    # Create the array of the right shape to feed into the keras model
                    # The 'length' or number of images you can put into the array is
                    # determined by the first position in the shape tuple, in this case 1.
                    data = pd.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

                    # Replace this with the path to your image
                    #image = Image.open('C:\\Users\\acer\\Pictures\\Saved Pictures\\person 2.jpg')
                    image = Image.open()

                    #resize the image to a 224x224 with the same strategy as in TM2:
                    #resizing the image to be at least 224x224 and then cropping from the center
                    size = (224, 224)
                    image = ImageOps.fit(image, size, Image.ANTIALIAS)

                    #turn the image into a numpy array
                    image_array = pd.asarray(image)

                    

                    # Normalize the image
                    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

                    # Load the image into the array
                    data[0] = normalized_image_array

                # run the inference
                    prediction = model.predict(data)
                    print(prediction)

                    # condition checking
                    if prediction[0][1] > prediction[0][0]:
                    
                      
                      return redirect('/')
                    else:
                       webbrowser.open('https://akb-alphadebuggers-maps.glitch.me/')
                       return redirect('/')
                
    
    
 





    
