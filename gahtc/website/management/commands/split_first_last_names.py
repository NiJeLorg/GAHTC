import sys,os
from django.core.management.base import BaseCommand, CommandError
from website.models import *

class Command(BaseCommand):
    
    def split_first_last(self):
        profiles = profile.objects.all()

        for p in profiles:
        	try:
				s = p.name.split()
				print s
				last_name = s[-1]
				first_name = s[:-1]
				first_name = ' '.join(first_name)
				p.first_name = first_name
				p.last_name = last_name
				p.save()
        	except Exception as e:
        		print e


    def handle(self, *args, **options):
        print "Split 'Name' into First and Last Names...."
        self.split_first_last()
        print "Done."



