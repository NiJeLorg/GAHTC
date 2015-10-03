from django.shortcuts import render
from django.http import HttpResponseRedirect
import operator
from django.db.models import TextField, CharField, Q, Count
from django.contrib.auth.decorators import login_required


# import all website models
from website.models import *

# GAHTC Views
def index(request):
	"""
	  Index page
	"""
	context_dict = {}
	return render(request, 'website/index.html', context_dict)


@login_required
def search(request):
	"""
	  Queries the database for search terms and returns list of results
	"""

	# search terms
	try:
		keyword = request.POST['keyword']
	except KeyError:
		return HttpResponseRedirect("/")
	
	# empty search strings and query Qs
	modules_keywords_query = Q()
	module_documents_keywords_query = Q()
	lectures_keywords_query = Q()
	lecture_documents_keywords_query = Q()
	lecture_slides_keywords_query = Q()

	if(keyword != ""):
		# group of keyword queries for text in modules documents
		modules_fields = [f for f in modules._meta.fields if (isinstance(f, TextField)) or (isinstance(f, CharField))]
		modules_queries = [Q(**{"%s__icontains" % f.name: keyword}) for f in modules_fields]
		for q in modules_queries:
			modules_keywords_query = modules_keywords_query | q 

		# group of keyword queries for text in modules documents
		module_documents_fields = [f for f in moduleDocuments._meta.fields if (isinstance(f, TextField)) or (isinstance(f, CharField))]
		module_documents_queries = [Q(**{"%s__icontains" % f.name: keyword}) for f in module_documents_fields]
		for q in module_documents_queries:
			module_documents_keywords_query = module_documents_keywords_query | q

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
		# group of keyword queries for text in lecture slides
		lecture_slides_fields = [f for f in lectureSlides._meta.fields if (isinstance(f, TextField)) or (isinstance(f, CharField))]
		lecture_slides_queries = [Q(**{"%s__icontains" % f.name: keyword}) for f in lecture_slides_fields]
		for q in lecture_slides_queries:
			lecture_slides_keywords_query = lecture_slides_keywords_query | q


	# get count and if no objects returned, send to different tempalate
	modules_returned_count = modules.objects.filter(modules_keywords_query).count()
	module_documents_returned_count = moduleDocuments.objects.filter(module_documents_keywords_query).count()
	lectures_returned_count = lectures.objects.filter(lectures_keywords_query).count()
	lecture_documents_returned_count = lectureDocuments.objects.filter(lecture_documents_keywords_query).count()
	lecture_slides_returned_count = lectureSlides.objects.filter(lecture_slides_keywords_query).count()

	if (modules_returned_count == 0 and module_documents_returned_count == 0 lectures_returned_count == 0 and lecture_documents_returned_count == 0 and lecture_slides_returned_count == 0):
		context_dict = {'keyword':keyword}
		return render(request, 'website/no_search_results.html', context_dict)
	else:
		modules_returned = modules.objects.filter(modules_keywords_query)
		module_documents_returned = moduleDocuments.objects.filter(module_documents_keywords_query)
		lectures_returned = lectures.objects.filter(lectures_keywords_query)
		lecture_documents_returned = lectureDocuments.objects.filter(lecture_documents_keywords_query)[:50]
		lecture_slides_returned = lectureSlides.objects.filter(lecture_slides_keywords_query)[:50]

		for lecture in lectures_returned:
			lecture.count = lecture.presentation_text.lower().count(keyword.lower()) + lecture.title.lower().count(keyword.lower()) + lecture.authors.lower().count(keyword.lower())

		lectures_returned = sorted(lectures_returned, key=operator.attrgetter('count'), reverse=True)

		# pull bundles
		bundles_returned = bundles.objects.filter(user=request.user)

		context_dict = {'keyword':keyword, 'modules_returned':modules_returned, 'lectures_returned':lectures_returned, 'lecture_documents_returned':lecture_documents_returned, 'lecture_slides_returned':lecture_slides_returned, 'bundles_returned':bundles_returned, 'modules_returned_count':modules_returned_count, 'lectures_returned_count':lectures_returned_count, 'lecture_documents_returned_count':lecture_documents_returned_count, 'lecture_slides_returned_count':lecture_slides_returned_count}
		return render(request, 'website/search.html', context_dict)
	


def showModule(request, id=None):
	"""
	  Response from AJAX request to show module in sidebar
	"""
	#get module
	module_returned = modules.objects.get(pk=id)

	#get first lecture uploaded
	earliest_lecture = lectures.objects.filter(module=module_returned).earliest('created')

	# pull bundles
	bundles_returned = bundles.objects.filter(user=request.user)

	context_dict = {'module_returned':module_returned, 'earliest_lecture':earliest_lecture, 'bundles_returned':bundles_returned}
	return render(request, 'website/show_module.html', context_dict)

def showLecture(request, id=None):
	"""
	  Response from AJAX request to show lecture in sidebar
	"""
	#get lecture
	lecture_returned = lectures.objects.get(pk=id)

	# pull bundles
	bundles_returned = bundles.objects.filter(user=request.user)

	context_dict = {'lecture_returned':lecture_returned, 'bundles_returned':bundles_returned}
	return render(request, 'website/show_lecture.html', context_dict)

def showLectureDocument(request, id=None):
	"""
	  Response from AJAX request to show lecture document in sidebar
	"""
	#get lecture document
	lecture_document_returned = lectureDocuments.objects.get(pk=id)

	# pull bundles
	bundles_returned = bundles.objects.filter(user=request.user)

	context_dict = {'lecture_document_returned':lecture_document_returned, 'bundles_returned':bundles_returned}
	return render(request, 'website/show_lecture_document.html', context_dict)

def showLectureSlide(request, id=None):
	"""
	  Response from AJAX request to show lecture slide in sidebar
	"""
	#get lecture slide
	lecture_slide_returned = lectureSlides.objects.get(pk=id)

	# pull bundles
	bundles_returned = bundles.objects.filter(user=request.user)

	context_dict = {'lecture_slide_returned':lecture_slide_returned, 'bundles_returned':bundles_returned}
	return render(request, 'website/show_lecture_slide.html', context_dict)


def createNewBundle(request):
	"""
	  AJAX request to create new bundle and attach an item to the bundle
	"""

	if request.method == 'GET':
		#gather variables from get request
		title = request.GET.get("title","")
		itemid = request.GET.get("itemid","")

		# create bundle
		bundle = bundles(user=request.user, title=title)
		bundle.save()

		# add item to appropriate bundle 
		itemid = itemid.split("_")
		if itemid[0] == 'module':
			#look up module
			module = modules.objects.get(pk=itemid[1])
			bm = bundleModule(bundle=bundle, module=module)
			bm.save()
		elif itemid[0] == 'lecture':
			#look up lecture
			lecture = lectures.objects.get(pk=itemid[1])
			bl = bundleLecture(bundle=bundle, lecture=lecture)
			bl.save()
		elif itemid[0] == 'lecturedocument':
			#look up lectureDocument
			lectureDocument = lectureDocuments.objects.get(pk=itemid[1])
			bld = bundleLectureDocument(bundle=bundle, lectureDocument=lectureDocument)
			bld.save()
		else:
			#look up lectureSlide
			lectureSlide = lectureSlides.objects.get(pk=itemid[1])
			bls = bundleLectureSlides(bundle=bundle, lectureSlide=lectureSlide)
			bls.save()

	# pull bundles
	bundles_returned = bundles.objects.filter(user=request.user)


	context_dict = {'bundles_returned':bundles_returned}
	return render(request, 'website/bundle.html', context_dict)


def addToBundle(request):
	"""
	  AJAX request to attach an item to the bundle
	"""

	if request.method == 'GET':
		#gather variables from get request
		bundleid = request.GET.get("bundle","")
		itemid = request.GET.get("itemid","")

		# get bundle
		bundle = bundles.objects.get(pk=bundleid)

		# add item to appropriate bundle 
		itemid = itemid.split("_")
		if itemid[0] == 'module':
			#look up module
			module = modules.objects.get(pk=itemid[1])
			bm = bundleModule(bundle=bundle, module=module)
			bm.save()
		elif itemid[0] == 'lecture':
			#look up lecture
			lecture = lectures.objects.get(pk=itemid[1])
			bl = bundleLecture(bundle=bundle, lecture=lecture)
			bl.save()
		elif itemid[0] == 'lecturedocument':
			#look up lectureDocument
			lectureDocument = lectureDocuments.objects.get(pk=itemid[1])
			bld = bundleLectureDocument(bundle=bundle, lectureDocument=lectureDocument)
			bld.save()
		else:
			#look up lectureSlide
			lectureSlide = lectureSlides.objects.get(pk=itemid[1])
			bls = bundleLectureSlides(bundle=bundle, lectureSlide=lectureSlide)
			bls.save()

	# pull bundles
	bundles_returned = bundles.objects.filter(user=request.user)


	context_dict = {'bundles_returned':bundles_returned}
	return render(request, 'website/bundle.html', context_dict)



