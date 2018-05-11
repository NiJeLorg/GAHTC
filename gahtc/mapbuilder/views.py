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

	query = request.GET.get('q')
	if query:
		maps = Map.objects.filter(public=True, name__icontains=query)
	else:
		maps = Map.objects.filter(public=True).order_by('created_date')

	return render(request, 'mapbuilder/index.html',{'maps':maps})

@login_required
def startmap(request):
	query = request.GET.get('q')
	if query:
		maps = Map.objects.filter(public=True, name__icontains=query)
	else:
		maps = Map.objects.filter(public=True).order_by('created_date')[:4]
	return render(request, 'mapbuilder/start-map.html',{'maps':maps})

@login_required
def map(request):

	return render(request, 'mapbuilder/map.html')

@login_required
def mapextent(request):

	return render(request, 'mapbuilder/map-extent.html')

@login_required
def mapexport(request):
		# import pdb
		print request.POST
		# pdb.set_trace()
		if request.method == 'POST' and request.is_ajax():
				# import pdb; pdb.set_trace()
				map_id = request.POST.get('map_id')
				if not map_id or map_id == '':
					map_id = None
				else:
					map_id =int(map_id)
				print request.POST
				map_data = request.POST.get('map_data')
				map_name = request.POST.get('map_name')
				map_image = request.FILES.get('map_image')
				map, created = Map.objects.get_or_create(id=map_id, user=request.user)
				map.data = map_data
				map.name = map_name
				map.image = map_image
				# import pdb; pdb.set_trace()
				map.save()
				return HttpResponse(json.dumps({'map_id': map.id}), content_type="application/json")
		return render(request, 'mapbuilder/map-export.html')

@login_required
def mymaps(request):
	mymaps = Map.objects.filter(user=request.user)
	return render(request, 'mapbuilder/mymaps.html', {'mymaps':mymaps})