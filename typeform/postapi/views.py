from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status

import requests

class Index(View):
    def get(self, request):
        context = {}
        context['test'] = "i am paradox"
        #return HttpResponse("hello world")
        return render(request, 'postapi/index.html', context)

    def post(self, request):
        return HttpResponse("post page")

# CBV for our api
class Api(APIView):
    #renderer_classes = (JSONRenderer, )
    webhook_uri = "http://requestb.in/1d9da741"

    def get(self, request):
        data = request.GET
        return Response(request.data)

    def post(self, request, format=".json"):
        data = request.data
        response = requests.post(self.webhook_uri, data=data)
        return Response(data)
