from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from rest_framework.decorators import api_view
from django.core import exceptions, validators
from rest_framework.response import Response
import smtplib
import requests
import json
import os
import os.path
import base64
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageOps
from datetime import datetime
import re


# Create your views here.
@api_view(['GET', 'POST'])
def verify(request):
                
              if request.method== 'POST':
                    email = request.POST['email']
                    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
 
                    # Define a function for
                    # for validating an Email

 
                    # pass the regular expression
                    # and the string into the fullmatch() method
                    if(re.fullmatch(regex, email)):
                        return Response({"output":"Valid"})
 
                    else:
                        return Response({"output":"Invalid"})
                       
              else:
                return render(request,'emailverification.html')
   # [(0 is Happy), (1 is Angry), (2 is Sad), (3 is Fear)]


                      
                
    
    
 





    
