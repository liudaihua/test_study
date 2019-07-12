from django.shortcuts import render
from django.http import HttpResponse
# import the json
from django.http import JsonResponse

# import the logging library
import logging

# Create your views here.

def test(request):

   response = JsonResponse({'errCode': '0'})
   return response

