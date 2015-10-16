import os,zipfile
from django.shortcuts import render
from django.http import HttpResponseRedirect
import operator
from django.db.models import TextField, CharField, Q, Count
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.conf import settings

# path to media root for adding a zip archive
MEDIA_ROOT = settings.MEDIA_ROOT

# import all website models and forms
from website.models import *
from website.forms import *

# GAHTC Views
def index(request):
	"""
	  Index page
	"""
	context_dict = {}
	return render(request, 'website/index.html', context_dict)

def mainSearchCode(request, keyword, tab):
	"""
	  Queries the database for search terms and returns list of results -- used in search and bundles
	"""
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

	if (modules_returned_count == 0 and module_documents_returned_count == 0 and lectures_returned_count == 0 and lecture_documents_returned_count == 0 and lecture_slides_returned_count == 0):
		modules_returned = modules.objects.none()
		moduleDocsCount = moduleDocuments.objects.none()
		lectures_returned = lectures.objects.none()
		lecture_documents_returned = lectureDocuments.objects.none()
		lecture_slides_returned = lectureSlides.objects.none()

		# pull bundles
		bundles_returned = bundles.objects.filter(user=request.user)

		# pull user profile
		user_profile = profile.objects.get(user=request.user)

		context_dict = {'keyword':keyword, 'modules_returned':modules_returned, 'moduleDocsCount': moduleDocsCount, 'lectures_returned':lectures_returned, 'lecture_documents_returned':lecture_documents_returned, 'lecture_slides_returned':lecture_slides_returned, 'bundles_returned':bundles_returned, 'modules_returned_count':modules_returned_count, 'lectures_returned_count':lectures_returned_count, 'lecture_documents_returned_count':lecture_documents_returned_count, 'lecture_slides_returned_count':lecture_slides_returned_count, 'tab': tab, 'user_profile': user_profile}

	else:
		modules_returned = modules.objects.filter(modules_keywords_query)
		module_documents_returned = moduleDocuments.objects.filter(module_documents_keywords_query)
		lectures_returned = lectures.objects.filter(lectures_keywords_query)
		lecture_documents_returned = lectureDocuments.objects.filter(lecture_documents_keywords_query)[:100]
		lecture_slides_returned = lectureSlides.objects.filter(lecture_slides_keywords_query)[:100]

		# concatonate module querysets
		# first create list of modules
		module_documents_modules = []
		lectures_modules = []

		for module_document in module_documents_returned:
			module_documents_modules.append(module_document.module)

		for lecture in lectures_returned:
			lectures_modules.append(lecture.module)

		module_list = list(chain(modules_returned, module_documents_modules, lectures_modules))

		# make unique
		module_set = set(module_list)
		unique_module_list = list(module_set)
		unique_module_list_count = len(unique_module_list)

		#set for template
		modules_returned = unique_module_list
		modules_returned_count = unique_module_list_count
		
		# sort decending by number of times words show up in the list
		for module in modules_returned:
			# look up docs
			moduleDocsCount = moduleDocuments.objects.filter(module=module)
			#count number of times keyword comes up in docs
			moduleDocsWordCount = 0
			contents = []
			for doc in moduleDocsCount:
				moduleDocsWordCount = moduleDocsWordCount + doc.document_contents.lower().count(keyword.lower())
				#add document contents to modules
				contents.append(doc.document_contents)

			# join document contents together
			module.document_contents = '\n'.join(contents)

			# look up lectures
			lecturesCount = lectures.objects.filter(module=module)
			#count number of times keyword comes up in lectures
			lecturesWordCount = 0
			for lec in lecturesCount:
				lecturesWordCount = lecturesWordCount + lec.title.lower().count(keyword.lower()) + lec.authors.lower().count(keyword.lower()) + lec.presentation_text.lower().count(keyword.lower())

			module.count = module.title.lower().count(keyword.lower()) + module.authors.lower().count(keyword.lower()) + moduleDocsWordCount + lecturesWordCount

		modules_returned = sorted(modules_returned, key=operator.attrgetter('count'), reverse=True)


		for lecture in lectures_returned:
			lecture.count = lecture.presentation_text.lower().count(keyword.lower()) + lecture.title.lower().count(keyword.lower()) + lecture.authors.lower().count(keyword.lower())

		lectures_returned = sorted(lectures_returned, key=operator.attrgetter('count'), reverse=True)


		for lectureDocs in lecture_documents_returned:
			lectureDocs.count = lectureDocs.document_contents.lower().count(keyword.lower())

		lecture_documents_returned = sorted(lecture_documents_returned, key=operator.attrgetter('count'), reverse=True)


		for lectureSlide in lecture_slides_returned:
			lectureSlide.count = lectureSlide.slide_main_text.lower().count(keyword.lower()) + lectureSlide.slide_notes.lower().count(keyword.lower())

		lecture_slides_returned = sorted(lecture_slides_returned, key=operator.attrgetter('count'), reverse=True)


		# pull bundles
		bundles_returned = bundles.objects.filter(user=request.user)

		# pull user profile
		user_profile = profile.objects.get(user=request.user)

		context_dict = {'keyword':keyword, 'modules_returned':modules_returned, 'moduleDocsCount': moduleDocsCount, 'lectures_returned':lectures_returned, 'lecture_documents_returned':lecture_documents_returned, 'lecture_slides_returned':lecture_slides_returned, 'bundles_returned':bundles_returned, 'modules_returned_count':modules_returned_count, 'lectures_returned_count':lectures_returned_count, 'lecture_documents_returned_count':lecture_documents_returned_count, 'lecture_slides_returned_count':lecture_slides_returned_count, 'tab': tab, 'user_profile': user_profile}

	return context_dict


@login_required
def search(request):
	"""
	  Queries the database for search terms and returns list of results
	"""

	# search terms
	try:
		keyword = request.POST['keyword']
		tab = 'search'
		context_dict = mainSearchCode(request, keyword, tab)
	except KeyError:
		return HttpResponseRedirect("/")
	
	return render(request, 'website/profile.html', context_dict)


@login_required
def mybundles(request):
	"""
	  Queries the database for search terms and returns list of results; goes to bundle
	"""

	# placeholder keyword to return all items
	keyword = 'Architecture'
	tab = 'bundle'
	context_dict = mainSearchCode(request, keyword, tab)	

	return render(request, 'website/profile.html', context_dict)


@login_required
def myprofile(request):
	"""
	  Queries the database for search terms and returns list of results; goes to bundle
	"""

	# placeholder keyword to return all items
	keyword = 'Architecture'
	tab = 'profile'
	context_dict = mainSearchCode(request, keyword, tab)	

	return render(request, 'website/profile.html', context_dict)




def showModule(request, id=None):
	"""
	  Response from AJAX request to show module in sidebar
	"""
	#get module
	module_returned = modules.objects.get(pk=id)

	#look up module docs 
	moduleDocs = moduleDocuments.objects.filter(module=module_returned)
	# just get the file name
	for doc in moduleDocs:
		document = str(doc.document)
		document = document.split('/')
		doc.documentName = document[2]

	#look up the lectures
	moduleLecs = lectures.objects.filter(module=module_returned)
	# get the file name
	for lec in moduleLecs:
		lecture = str(lec.presentation)
		lecture = lecture.split('/')
		lec.lectureName = lecture[2]
		# get lecture documents
		lectureDocs = lectureDocuments.objects.filter(lecture=lec)
		lec.lectureDocs = lectureDocs
		for lecDoc in lec.lectureDocs:
			document = str(lecDoc.document)
			document = document.split('/')
			lecDoc.documentName = document[2]



	moduleDocsCount = moduleDocuments.objects.filter(module=module_returned)
	contents = []
	for doc in moduleDocsCount:
		#add document contents to modules
		contents.append(doc.document_contents)

	# join document contents together
	module_returned.document_contents = '\n'.join(contents)	

	#get first lecture uploaded
	earliest_lecture = lectures.objects.filter(module=module_returned).earliest('created')

	# pull bundles
	bundles_returned = bundles.objects.filter(user=request.user)

	context_dict = {'module_returned':module_returned, 'earliest_lecture':earliest_lecture, 'bundles_returned':bundles_returned, 'moduleDocs':moduleDocs, 'moduleLecs':moduleLecs}
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
	return render(request, 'website/bundle_dropdown.html', context_dict)


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
			#does bundle/module exist already?
			if bundleModule.objects.filter(bundle=bundle, module=module).exists() == False:
				bm = bundleModule(bundle=bundle, module=module)
				bm.save()
		elif itemid[0] == 'lecture':
			#look up lecture
			lecture = lectures.objects.get(pk=itemid[1])
			if bundleLecture.objects.filter(bundle=bundle, lecture=lecture).exists() == False:
				bl = bundleLecture(bundle=bundle, lecture=lecture)
				bl.save()
		elif itemid[0] == 'lecturedocument':
			#look up lectureDocument
			lectureDocument = lectureDocuments.objects.get(pk=itemid[1])
			if bundleLectureDocument.objects.filter(bundle=bundle, lectureDocument=lectureDocument).exists() == False:
				bld = bundleLectureDocument(bundle=bundle, lectureDocument=lectureDocument)
				bld.save()
		else:
			#look up lectureSlide
			lectureSlide = lectureSlides.objects.get(pk=itemid[1])
			if bundleLectureSlides.objects.filter(bundle=bundle, lectureSlide=lectureSlide).exists() == False:
				bls = bundleLectureSlides(bundle=bundle, lectureSlide=lectureSlide)
				bls.save()

	# pull bundles
	bundles_returned = bundles.objects.filter(user=request.user)


	context_dict = {'bundles_returned':bundles_returned}
	return render(request, 'website/bundle_dropdown.html', context_dict)


def removeFromBundle(request):
	"""
	  AJAX request to remove an item to the bundle
	"""

	if request.method == 'GET':
		#gather variables from get request
		bundleid = request.GET.get("bundle","")
		itemid = request.GET.get("itemid","")
		typename = request.GET.get("type","")

		# get bundle
		bundle = bundles.objects.get(pk=bundleid)

		# remove item from appropriate bundle 
		if typename == 'module':
			#look up module
			module = modules.objects.get(pk=itemid)
			bm = bundleModule.objects.filter(bundle=bundle, module=module)
			for rec in bm:
				rec.delete()
			
		elif typename == 'lecture':
			#look up lecture
			lecture = lectures.objects.get(pk=itemid)
			bl = bundleLecture.objects.filter(bundle=bundle, lecture=lecture)
			for rec in bl:
				rec.delete()

		elif typename == 'lecturedocument':
			#look up lectureDocument
			lectureDocument = lectureDocuments.objects.get(pk=itemid)
			bld = bundleLectureDocument.objects.filter(bundle=bundle, lectureDocument=lectureDocument)
			for rec in bld:
				rec.delete()
		else:
			#look up lectureSlide
			lectureSlide = lectureSlides.objects.get(pk=itemid)
			bls = bundleLectureSlides.objects.filter(bundle=bundle, lectureSlide=lectureSlide)
			for rec in bls:
				bls.delete()

	# pull bundles
	bundles_returned = bundles.objects.filter(user=request.user)


	context_dict = {'bundles_returned':bundles_returned}
	return render(request, 'website/bundle_dropdown.html', context_dict)


def showBundle(request, id=None):
	"""
	  Response from AJAX request to show bundle in sidebar
	"""
	#get lecture slide
	bundle_returned = bundles.objects.get(pk=id, user=request.user)

	#get return all other content
	bundle_modules = bundleModule.objects.filter(bundle=bundle_returned)
	bundle_lectures = bundleLecture.objects.filter(bundle=bundle_returned)
	bundle_lecture_documents = bundleLectureDocument.objects.filter(bundle=bundle_returned)
	bundle_lecture_slides = bundleLectureSlides.objects.filter(bundle=bundle_returned)

	# for each module in a bundle, attach the module documents and the lectures
	for bundle in bundle_modules:
		#look up module docs 
		moduleDocs = moduleDocuments.objects.filter(module=bundle.module)
		# just get the file name
		for doc in moduleDocs:
			document = str(doc.document)
			document = document.split('/')
			doc.documentName = document[2]

		#attach to the bundle
		bundle.module.moduleDocs = moduleDocs

		#look up the lectures
		moduleLecs = lectures.objects.filter(module=bundle.module)
		# get the file name
		for lec in moduleLecs:
			lecture = str(lec.presentation)
			lecture = lecture.split('/')
			lec.lectureName = lecture[2]
			# get lecture documents
			lectureDocs = lectureDocuments.objects.filter(lecture=lec)
			lec.lectureDocs = lectureDocs
			for lecDoc in lec.lectureDocs:
				document = str(lecDoc.document)
				document = document.split('/')
				lecDoc.documentName = document[2]

		bundle.module.lectures = moduleLecs


	#for each lecture document strip out name of file
	for bundle in bundle_lecture_documents:
		document = str(bundle.lectureDocument.document)
		document = document.split('/')
		bundle.lectureDocument.documentName = document[2]

	#for each lecture slide strip out name of file and slide notes file
	for bundle in bundle_lecture_slides:
		slide = str(bundle.lectureSlide.slide)
		slide = slide.split('/')
		bundle.lectureSlide.slideName = slide[2]
		slideNotes = str(bundle.lectureSlide.slide_notes_document)
		slideNotes = slideNotes.split('/')
		bundle.lectureSlide.slideNotesName = slideNotes[2]


	context_dict = {'bundle_returned':bundle_returned, 'bundle_modules':bundle_modules, 'bundle_lectures': bundle_lectures, 'bundle_lecture_documents': bundle_lecture_documents, 'bundle_lecture_slides': bundle_lecture_slides}
	return render(request, 'website/show_bundle.html', context_dict)


def zipUpBundle(request, id=None):
	"""
	  Response from AJAX request to zip up bundle and create download
	"""
	#folder for zip file
	folder = "/zip_files/"+ id +"/"
	filename = "GAHTC_bundle_"+ id +".zip"
	zipfolder = "GAHTC_bundle_"+ id

	if not os.path.exists(MEDIA_ROOT + folder):
		os.makedirs(MEDIA_ROOT + folder)

	#create zip file
	with zipfile.ZipFile(MEDIA_ROOT + folder + filename, "w", allowZip64=True) as myzip:

		#get lecture slide
		bundle_returned = bundles.objects.get(pk=id, user=request.user)

		#get return all other content
		bundle_modules = bundleModule.objects.filter(bundle=bundle_returned)
		bundle_lectures = bundleLecture.objects.filter(bundle=bundle_returned)
		bundle_lecture_documents = bundleLectureDocument.objects.filter(bundle=bundle_returned)
		bundle_lecture_slides = bundleLectureSlides.objects.filter(bundle=bundle_returned)

		# for each module in a bundle, attach the module documents and the lectures
		for bundle in bundle_modules:
			# create directory for module

			#look up module docs 
			moduleDocs = moduleDocuments.objects.filter(module=bundle.module)
			#loop over docs and add to zip archive in the correct folder
			for doc in moduleDocs:
				modTitle = ''.join(bundle.module.title.split())
				document = str(doc.document)
				document = document.split('/')
				directory = os.path.join(zipfolder+ "/modules/" + modTitle + "/documents", document[2])
				myzip.write(MEDIA_ROOT + '/' + str(doc.document), directory)

			#look up the lectures
			moduleLecs = lectures.objects.filter(module=bundle.module)
			#loop over lectures and add to zip archive in the correct folder
			for lec in moduleLecs:
				modTitle = ''.join(bundle.module.title.split())
				lecTitle = ''.join(lec.title.split())
				document = str(lec.presentation)
				document = document.split('/')
				directory = os.path.join(zipfolder+ "/modules/" + modTitle + "/lectures/" + lecTitle, document[2])
				myzip.write(MEDIA_ROOT + '/' + str(lec.presentation), directory)

				# look up lecture documents
				moduleLecDocs = lectureDocuments.objects.filter(lecture=lec)
				for lecDoc in moduleLecDocs:
					document = str(lecDoc.document)
					document = document.split('/')
					directory = os.path.join(zipfolder+ "/modules/" + modTitle + "/lectures/" + lecTitle, document[2])
					myzip.write(MEDIA_ROOT + '/' + str(lecDoc.document), directory)


		# for each lecture write to zip archive 
		for bundle in bundle_lectures:
			lecTitle = ''.join(bundle.lecture.title.split())
			document = str(bundle.lecture.presentation)
			document = document.split('/')
			directory = os.path.join(zipfolder+ "/lectures/" + lecTitle, document[2])
			myzip.write(MEDIA_ROOT + '/' + str(bundle.lecture.presentation), directory)

			# look up lecture documents and add these to zip archive
			lecDocs = lectureDocuments.objects.filter(lecture=bundle.lecture)
			for lecDoc in lecDocs:
				document = str(lecDoc.document)
				document = document.split('/')
				directory = os.path.join(zipfolder+ "/lectures/" + lecTitle, document[2])
				myzip.write(MEDIA_ROOT + '/' + str(lecDoc.document), directory)


		#for each lecture document strip out name of file
		for bundle in bundle_lecture_documents:
			lecTitle = ''.join(bundle.lectureDocument.lecture.title.split())	
			document = str(bundle.lectureDocument.document)
			document = document.split('/')
			directory = os.path.join(zipfolder+ "/lecture_documents/" + lecTitle, document[2])
			myzip.write(MEDIA_ROOT + '/' + str(bundle.lectureDocument.document), directory)

		#for each lecture slide strip out name of file and slide notes file
		for bundle in bundle_lecture_slides:
			lecTitle = ''.join(bundle.lectureSlide.lecture.title.split())	
			document = str(bundle.lectureSlide.slide)
			document = document.split('/')
			directory = os.path.join(zipfolder+ "/lecture_slides/" + lecTitle, document[2])
			myzip.write(MEDIA_ROOT + '/' + str(bundle.lectureSlide.slide), directory)
			document = str(bundle.lectureSlide.slide_notes_document)
			document = document.split('/')			
			directory = os.path.join(zipfolder+ "/lecture_slides/" + lecTitle, document[2])
			myzip.write(MEDIA_ROOT + '/' + str(bundle.lectureSlide.slide_notes_document), directory)

	#get size of zip file
	filesize = os.path.getsize(MEDIA_ROOT + folder + filename)

	context_dict = {'folder':folder, 'filename':filename, 'filesize':filesize}
	return render(request, 'website/bundle_download.html', context_dict)


def zipUpModule(request, id=None):
	"""
	  Response from AJAX request to zip up module and create download
	"""
	#folder for zip file
	folder = "/zip_files/module_"+ id +"/"
	filename = "GAHTC_module_"+ id +".zip"
	zipfolder = "GAHTC_module_"+ id

	if not os.path.exists(MEDIA_ROOT + folder):
		os.makedirs(MEDIA_ROOT + folder)

	#create zip file
	with zipfile.ZipFile(MEDIA_ROOT + folder + filename, "w", allowZip64=True) as myzip:

		#get module
		module_returned = modules.objects.get(pk=id)

		#look up module docs 
		moduleDocs = moduleDocuments.objects.filter(module=module_returned)
		#loop over docs and add to zip archive in the correct folder
		for doc in moduleDocs:
			modTitle = ''.join(module_returned.title.split())
			document = str(doc.document)
			document = document.split('/')
			directory = os.path.join(zipfolder+ "/modules/" + modTitle + "/documents", document[2])
			myzip.write(MEDIA_ROOT + '/' + str(doc.document), directory)

		#look up the lectures
		moduleLecs = lectures.objects.filter(module=module_returned)
		#loop over lectures and add to zip archive in the correct folder
		for lec in moduleLecs:
			modTitle = ''.join(module_returned.title.split())
			lecTitle = ''.join(lec.title.split())
			document = str(lec.presentation)
			document = document.split('/')
			directory = os.path.join(zipfolder+ "/modules/" + modTitle + "/lectures/" + lecTitle, document[2])
			myzip.write(MEDIA_ROOT + '/' + str(lec.presentation), directory)

			# look up lecture documents
			moduleLecDocs = lectureDocuments.objects.filter(lecture=lec)
			for lecDoc in moduleLecDocs:
				document = str(lecDoc.document)
				document = document.split('/')
				directory = os.path.join(zipfolder+ "/modules/" + modTitle + "/lectures/" + lecTitle, document[2])
				myzip.write(MEDIA_ROOT + '/' + str(lecDoc.document), directory)



	#get size of zip file
	filesize = os.path.getsize(MEDIA_ROOT + folder + filename)

	context_dict = {'folder':folder, 'filename':filename, 'filesize':filesize}
	return render(request, 'website/bundle_download.html', context_dict)


def zipUpLecture(request, id=None):
	"""
	  Response from AJAX request to zip up lectures and create download
	"""
	#folder for zip file
	folder = "/zip_files/lecture_"+ id +"/"
	filename = "GAHTC_lecture_"+ id +".zip"
	zipfolder = "GAHTC_lecture_"+ id

	if not os.path.exists(MEDIA_ROOT + folder):
		os.makedirs(MEDIA_ROOT + folder)

	#create zip file
	with zipfile.ZipFile(MEDIA_ROOT + folder + filename, "w", allowZip64=True) as myzip:

		#get lecture
		lec = lectures.objects.get(pk=id)

		lecTitle = ''.join(lec.title.split())
		document = str(lec.presentation)
		document = document.split('/')
		directory = os.path.join(zipfolder+ "/lectures/" + lecTitle, document[2])
		myzip.write(MEDIA_ROOT + '/' + str(lec.presentation), directory)

		# look up lecture documents
		lecDocs = lectureDocuments.objects.filter(lecture=lec)
		for lecDoc in lecDocs:
			document = str(lecDoc.document)
			document = document.split('/')
			directory = os.path.join(zipfolder+ "/lectures/" + lecTitle, document[2])
			myzip.write(MEDIA_ROOT + '/' + str(lecDoc.document), directory)



	#get size of zip file
	filesize = os.path.getsize(MEDIA_ROOT + folder + filename)

	context_dict = {'folder':folder, 'filename':filename, 'filesize':filesize}
	return render(request, 'website/bundle_download.html', context_dict)



def refreshSidebarBundle(request):

	# pull bundles
	bundles_returned = bundles.objects.filter(user=request.user)


	context_dict = {'bundles_returned':bundles_returned}
	return render(request, 'website/bundle_list.html', context_dict)



@login_required
def updateProfile(request):
	"""
	  Loads the user profile page for editing
	"""	


	#get user profile data and pass to view
	try:
		user_profile = profile.objects.get(user=request.user)
	except profile.DoesNotExist:
		user_profile = None
		
	if request.method == 'POST':
		user_form = UserInfoForm(data=request.POST, instance=request.user)
		profile_form = UserProfileForm(data=request.POST, instance=user_profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()       
			pf = profile_form.save(commit=False)
			pf.pic = request.FILES['pic'] 
			pf.user = request.user
			pf.save()

			return HttpResponseRedirect("/profile/")
						
		else:
			print user_form.errors, profile_form.errors
			
	else:
		user_form = UserInfoForm(instance=request.user)
		profile_form = UserProfileForm(instance=user_profile)


	keyword = 'Architecture'
	tab = 'profile'
	context_dict = mainSearchCode(request, keyword, tab)	

	context_dict_extra = {'user_form': user_form, 'profile_form': profile_form}

	context_dict.update(context_dict_extra)

	return render(request, 'website/update_profile.html', context_dict)


@login_required
def modulesView(request):
	"""
	  Loads all modules 
	"""	

	modules_returned = modules.objects.all()

	for module_returned in modules_returned:
		#look up module docs 
		moduleDocs = moduleDocuments.objects.filter(module=module_returned)
		# just get the file name
		contents = []
		for doc in moduleDocs:
			document = str(doc.document)
			document = document.split('/')
			doc.documentName = document[2]
			contents.append(doc.document_contents)

		# join document contents together
		module_returned.document_contents = '\n'.join(contents)	

		#attach the module docs to the module returned 
		module_returned.moduleDocs = moduleDocs

		#look up the lectures
		moduleLecs = lectures.objects.filter(module=module_returned)
		# get the file name
		for lec in moduleLecs:
			lecture = str(lec.presentation)
			lecture = lecture.split('/')
			lec.lectureName = lecture[2]
			# get lecture documents
			lectureDocs = lectureDocuments.objects.filter(lecture=lec)
			lec.lectureDocs = lectureDocs
			for lecDoc in lec.lectureDocs:
				document = str(lecDoc.document)
				document = document.split('/')
				lecDoc.documentName = document[2]

		#attach the module docs to the module returned 
		module_returned.moduleLecs = moduleLecs


	context_dict = {'modules_returned':modules_returned}
	return render(request, 'website/modules.html', context_dict)



@login_required
def lecturesView(request):
	"""
	  Loads all lectures 
	"""	

	lectures_returned = lectures.objects.all()

	for lec in lectures_returned:
		lecture = str(lec.presentation)
		lecture = lecture.split('/')
		lec.lectureName = lecture[2]
		# get lecture documents
		lectureDocs = lectureDocuments.objects.filter(lecture=lec)
		lec.lectureDocs = lectureDocs
		for lecDoc in lec.lectureDocs:
			document = str(lecDoc.document)
			document = document.split('/')
			lecDoc.documentName = document[2]


	context_dict = {'lectures_returned':lectures_returned}
	return render(request, 'website/lectures.html', context_dict)


