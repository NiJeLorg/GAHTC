import datetime
from haystack import indexes
from website.models import *


class modulesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return modules

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())

class moduleDocumentsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return moduleDocuments

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())

class lecturesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return lectures

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())

class lectureSegmentsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return lectureSegments

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())

class lectureDocumentsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return lectureDocuments

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())

class lectureSlidesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return lectureSlides

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())

class comingSoonModulesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return comingSoonModules

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())



