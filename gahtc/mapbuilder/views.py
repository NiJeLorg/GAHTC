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

	return render(request, 'mapbuilder/start-map.html')