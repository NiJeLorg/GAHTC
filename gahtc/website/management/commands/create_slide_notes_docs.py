import sys,os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File
from website.models import *

"""
  creates text files from slide notes
"""
# path to media root for textract to find files
MEDIA_ROOT = settings.MEDIA_ROOT


class Command(BaseCommand):

    def create_text_files(self):
        # pull files from database
        lectureSlidesObjects = lectureSlides.objects.filter(extracted=False)

        # loop through modules and pull all text
        for ls in lectureSlidesObjects:
            # temporarily stick a file at the media root
            with open(MEDIA_ROOT + "/slide-"+ str(ls.slide_number) +".txt", "w+") as f:

                # create django file and save to DB
                textfile = File(f)
                textfile.write(ls.slide_notes.encode('utf-8').strip())
                ls.slide_notes_document.save("/slide-"+ str(ls.slide_number) +".txt", textfile)
                textfile.closed
                f.closed
                ls.extracted = True
                ls.save()

            os.remove(MEDIA_ROOT + "/slide-"+ str(ls.slide_number) +".txt")


    def handle(self, *args, **options):
        print "Create text files from slide notes...."
        self.create_text_files()
        print "Done."





