# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Map

from django.http import HttpResponse
import string
from base64 import b64decode
from django.core.files.base import ContentFile
import os
from datetime import datetime
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def index(request):

	query = request.GET.get('q')
	if query:
		maps = Map.objects.filter(public=True, name__icontains=query).order_by('-created_date')
	else:
		maps = Map.objects.filter(public=True).order_by('-created_date')

	paginator = Paginator(maps, 10)
	page = request.GET.get('page')
	try:
		maps = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		maps = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		maps = paginator.page(paginator.num_pages)

	return render(request, 'mapbuilder/index.html',{'maps':maps})

@login_required
def startmap(request):
	query = request.GET.get('q')
	recentMap =  Map.objects.filter(user=request.user).order_by('-id')
	if query:
		maps = Map.objects.filter(public=True,  name__icontains=query)
	else:
		maps = Map.objects.filter(public=True).order_by('-created_date')
	if(len(recentMap)):
		recentMap = recentMap[0]
	if(len(maps)):
		maps = maps[:4]
	return render(request, 'mapbuilder/start-map.html',{'maps':maps, 'recentMap': recentMap})

@login_required
def map(request):

	return render(request, 'mapbuilder/map.html')

@login_required
def mapextent(request):

	return render(request, 'mapbuilder/map-extent.html')

@login_required
def mapexport(request, id=False):
		# import pdb
		# pdb.set_trace()
		# if not os.path.exists(os.path.join(settings.MEDIA_URL, 'mapbuilder')):
		# 	os.makedirs(os.path.join(settings.MEDIA_URL, 'mapbuilder'))
		currentMap = {'data': '', 'image': '', id: ''}
		if request.method == 'GET' and id:
			currentMap =   Map.objects.get(pk=id)

		elif request.method == 'POST' and request.is_ajax():
				# import pdb; pdb.set_trace()
				map_id = request.POST.get('map_id')
				if not map_id or map_id == '':
					map_id = None
				else:
					map_id =int(map_id)
				map_name = request.POST.get('map_name')
				if not map_name:
					map_name = 'untitled' + datetime.now().strftime('%Y-%m-%d')
				map_data = request.POST.get('map_data')
				map_image = request.POST.get('map_image')
				base_map_image = request.POST.get('base_map_image')
				public_map = request.POST.get('public_map')
				# print map_image
				# params, map_image = map_image.split(',', 1)
				# param2, base_map_image = base_map_image.split(',', 1)
				img_data = b64decode(map_image)
				base_map_data = b64decode(base_map_image)
				file_name_string = format_filename(map_name) + '.png'
				map, created = Map.objects.get_or_create(id=map_id, user=request.user)
				if public_map :
					map.public =True
				map.data = map_data
				map.name = file_name_string
				map.image =  ContentFile(img_data, file_name_string)
				map.base_map_image =  ContentFile(base_map_data, file_name_string)
				map.save()
				return HttpResponse(json.dumps({'map_id': map.id}), content_type="application/json")
		return render(request, 'mapbuilder/map-export.html', {'map': currentMap})

@login_required
def mymaps(request):
	query = request.GET.get('q')
	if query:
		mymaps = Map.objects.filter(public=True, user=request.user, name__icontains=query).order_by('-created_date')
	else:
		mymaps = Map.objects.filter(public=True, user=request.user).order_by('-created_date')
	paginator = Paginator(mymaps, 10)
	page = request.GET.get('page')
	try:
		mymaps = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		mymaps = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		mymaps = paginator.page(paginator.num_pages)
	return render(request, 'mapbuilder/mymaps.html', {'mymaps':mymaps})


def format_filename(s):
	"""Take a string and return a valid filename constructed from the string.
Uses a whitelist approach: any characters not present in valid_chars are
removed. Also spaces are replaced with underscores.

Note: this method may produce invalid filenames such as ``, `.` or `..`
When I use this method I prepend a date string like '2009_01_15_19_46_32_'
and append a file extension like '.txt', so I avoid the potential of using
an invalid filename.

"""
	valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
	filename = ''.join(c for c in s if c in valid_chars)
	filename = filename.replace(' ', '_')  # I don't like spaces in filenames.


	return filename