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

	return render(request, 'mapbuilder/index.html')

def startmap(request):

	"""
	  Index page
	"""

	return render(request, 'mapbuilder/start-map.html', context={'GOOGLE_MAPS_API': settings.GOOGLE_MAPS_API})

def map(request):


	"""
	  map page
	"""

	return render(request, 'mapbuilder/map.html', context={'GOOGLE_MAPS_API': settings.GOOGLE_MAPS_API})

def mapextent(request):


	"""
	  map page
	"""

	return render(request, 'mapbuilder/map-extent.html', context={'GOOGLE_MAPS_API': settings.GOOGLE_MAPS_API})