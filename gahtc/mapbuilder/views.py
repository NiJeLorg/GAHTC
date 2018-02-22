# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import render

from django.http import HttpResponse




# Create your views here.

def index(request):


	"""
	  Index page
	"""

	return render(request, 'index.html')
def searchmap(request):


	"""
	  search page
	"""

	return render(request, 'search-map.html')
def startmap(request):


	"""
	  start page
	"""

	return render(request, 'start-map.html', context={'GOOGLE_MAPS_API': settings.GOOGLE_MAPS_API})
