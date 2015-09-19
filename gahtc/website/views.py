from django.shortcuts import render
import operator
from django.db.models import TextField, CharField
from django.db.models import Q


# import all website models
from website.models import *

# GAHTC Views
def index(request):
	"""
	  Index page
	"""
	context_dict = {}
	return render(request, 'website/index.html', context_dict)


def search(request):
	"""
	  Queries the database for search terms and returns list of results
	"""
	# empty search strings and query Qs
	modules_keywords_query = Q()
	lectures_keywords_query = Q()
	lecture_documents_keywords_query = Q()

	# search terms
	keyword = request.POST['keyword']

	if(keyword != ""):
		# group of keyword queries for text in modules documents
		modules_fields = [f for f in modules._meta.fields if (isinstance(f, TextField)) or (isinstance(f, CharField))]
		modules_queries = [Q(**{"%s__icontains" % f.name: keyword}) for f in modules_fields]
		for q in modules_queries:
			modules_keywords_query = modules_keywords_query | q       

		# group of keyword queries for text in lectures
		lectures_fields = [f for f in lectures._meta.fields if (isinstance(f, TextField)) or (isinstance(f, CharField))]
		lectures_queries = [Q(**{"%s__icontains" % f.name: keyword}) for f in lectures_fields]
		for q in lectures_queries:
			lectures_keywords_query = lectures_keywords_query | q       

		# group of keyword queries for text in lecture documents
		lecture_documents_fields = [f for f in lectureDocuments._meta.fields if (isinstance(f, TextField)) or (isinstance(f, CharField))]
		lecture_documents_queries = [Q(**{"%s__icontains" % f.name: keyword}) for f in lecture_documents_fields]
		for q in lecture_documents_queries:
			lecture_documents_keywords_query = lecture_documents_keywords_query | q       

	modulesreturned = modules.objects.filter(modules_keywords_query)
	lecturesreturned = lectures.objects.filter(lectures_keywords_query)
	lecture_documentsreturned = lectureDocuments.objects.filter(lecture_documents_keywords_query)


	context_dict = {'modulesreturned':modulesreturned, 'lecturesreturned':lecturesreturned, 'lecture_documentsreturned':lecture_documentsreturned}
	return render(request, 'website/search.html', context_dict)
	

