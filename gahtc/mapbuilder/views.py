# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse




# Create your views here.
@login_required
def index(request):

	"""
	  Index page
	"""

	return render(request, 'mapbuilder/index.html')

@login_required
def startmap(request):

	"""
	  Index page
	"""

	return render(request, 'mapbuilder/start-map.html')

@login_required
def map(request):


	"""
	  map page
	"""

	return render(request, 'mapbuilder/map.html')

@login_required
def mapextent(request):


	"""
	  map page
	"""

	return render(request, 'mapbuilder/map-extent.html')

@login_required
def mapexport(request):


	"""
	  map page
	"""

	return render(request, 'mapbuilder/map-export.html')