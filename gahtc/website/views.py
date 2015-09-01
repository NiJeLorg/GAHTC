from django.shortcuts import render

# import all website models
from website.models import *

# GAHTC Views
def index(request):
	context_dict = {}
	return render(request, 'website/index.html', context_dict)
