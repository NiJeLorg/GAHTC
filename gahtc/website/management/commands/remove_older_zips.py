import sys,os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File
from subprocess import call
from website.models import *

"""
  removes older zip files
"""

# path to media root for adding a zip archive
MEDIA_ROOT = settings.MEDIA_ROOT

class Command(BaseCommand):
    
    def remove_zips(self):
        # get all bundles and loop over them, removing zip files if they're present and older than 15 minutes
        bundleObjects = bundles.objects.all()

        for bundle in bundleObjects:

            path_to_file = MEDIA_ROOT + "/zip_files/" + str(bundle.id) + "/"
            print path_to_file
            call(["find",path_to_file,"-cmin","+10","-exec","rm","{}","+"])

    def handle(self, *args, **options):
        print "Removing Older Zip Files...."
        self.remove_zips()




