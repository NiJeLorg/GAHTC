# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Map

from django.http import HttpResponse




# Create your views here.
@login_required
def index(request):

	maps = Map.objects.filter(public=True).order_by('created_date')

	return render(request, 'mapbuilder/index.html',{'maps':maps})

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

		if request.method == 'POST' and request.is_ajax():
				map_id = request.POST.get('map_id')
				if map_id == '':
					map_id = None
				else:
					map_id =int(map_id)
				map_data = request.POST.get('map_data')
				map_name = request.POST.get('map_name')
				map, created = Map.objects.get_or_create(id=map_id, user=request.user)
				map.data = map_data
				map.name = map_name
				map.save()
				return HttpResponse(json.dumps({'map_id': map.id}), content_type="application/json")
		return render(request, 'mapbuilder/map-export.html')