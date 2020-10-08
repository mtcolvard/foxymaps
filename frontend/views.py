# from django.shortcuts import render
# def index(request):
#     return render(request, 'src/index.html')

import os
from django.views.generic import View
from django.http import HttpResponse, HttpResponseNotFound

class Home(View):

    def get(self, _request):
        with open(os.path.join(os.path.dirname(__file__), 'dist', 'index.html')) as file:
            return HttpResponse(file.read())
#
#
class Assets(View):

    def get(self, _request, filename):
        path = os.path.join(os.path.dirname(__file__), 'dist', filename)

        if os.path.isfile(path):
            with open(path, 'rb') as file:
            # with open(path) as file:
                return HttpResponse(file.read(), content_type='application/javascript')
        else:
            return HttpResponseNotFound()
