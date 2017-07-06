import sys,os,string
from django.core.management.base import BaseCommand, CommandError
from website.models import *

class Command(BaseCommand):
    
    def assign_modules(self):
        modules_objects = modules.objects.all()
        
        for m in modules_objects:
            # try to look up author last name in profiles, and if it exists, assign it to the module
            author_names_string = string.replace(m.authors, ',', '')
            author_names = author_names_string.strip().split()
            for name in author_names:          
                try:
                    profile_object = profile.objects.get(last_name=name)
                    if profile_object:
                        m.authors_m2m.add(profile_object)
                        #set as contributing member
                        profile_object.contributing = True
                        profile_object.save()
                except Exception as e:
                    print e

    def assign_lectures(self):
        lecture_objects = lectures.objects.all()
        
        for l in lecture_objects:
            # try to look up author last name in profiles, and if it exists, assign it to the lecture
            author_names_string = string.replace(l.authors, ',', '')
            author_names = author_names_string.strip().split()
            for name in author_names:          
                try:
                    profile_object = profile.objects.get(last_name=name)
                    if profile_object:
                        l.authors_m2m.add(profile_object)
                        #set as contributing member
                        profile_object.contributing = True
                        profile_object.save()
                except Exception as e:
                    print e

    def assign_cs_modules(self):
        modules_objects = comingSoonModules.objects.all()
        
        for m in modules_objects:
            # try to look up author last name in profiles, and if it exists, assign it to the module
            author_names_string = string.replace(m.authors, ',', '')
            author_names = author_names_string.strip().split()
            for name in author_names:          
                try:
                    profile_object = profile.objects.get(last_name=name)
                    if profile_object:
                        m.authors_m2m.add(profile_object)
                        #set as contributing member
                        profile_object.contributing = True
                        profile_object.save()
                except Exception as e:
                    print e

    def handle(self, *args, **options):
        print "Assign Authorship to Modules...."
        self.assign_modules()
        print "Assign Authorship to Lectures...."
        self.assign_lectures()
        print "Assign Authorship to Coming Soon Modules...."
        self.assign_cs_modules()
        print "Done."



