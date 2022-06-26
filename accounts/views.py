from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
import smtplib
import numpy as np
import tensorflow.keras
from PIL import Image, ImageOps
import webbrowser
from rest_framework.decorators import api_view
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
#@api_view(['GET'])       
def trashdetection(request):
                
               if request.method== 'POST':
                    data = {}
                   
                    img = request.FILES['img']
                    # Disable scientific notation for clarity
                    np.set_printoptions(suppress=True)

                    # Load the model
                    model = tensorflow.keras.models.load_model('keras_model (1).h5')

                    # Create the array of the right shape to feed into the keras model
                    # The 'length' or number of images you can put into the array is
                    # determined by the first position in the shape tuple, in this case 1.
                    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

                    # Replace this with the path to your image
                    # image = Image.open('trash1.jpg')
                    image = Image.open(img)

                    #resize the image to a 224x224 with the same strategy as in TM2:
                    #resizing the image to be at least 224x224 and then cropping from the center
                    size = (224, 224)
                    image = ImageOps.fit(image, size, Image.ANTIALIAS)

                    #turn the image into a numpy array
                    image_array = np.asarray(image)

                    

                    # Normalize the image
                    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

                    # Load the image into the array
                    data[0] = normalized_image_array

                    # run the inference
                    prediction = model.predict(data)
                    print(prediction)

                    # condition checking
                    if prediction[0][1] > prediction[0][0]:
                      answer = "clean"
                    else: 
                      answer = "trash"
                    data["output"] = answer
                    return data
                    #return redirect("accounts/trashorclean")
                    messages.info(request,data)

               else:
                      
                       return render(request,'trashdetection.html')

def trashorclean(request):
  return render(request, 'trashorclean.html')
                      
                
    
    
 





    
