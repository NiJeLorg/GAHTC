import sys,os
from django.core.management.base import BaseCommand, CommandError
from taggit.models import Tag


class Command(BaseCommand):
    
    def remove_tags(self):
        for tag in Tag.objects.all():
            tag.delete()


    def handle(self, *args, **options):
        print "Remove all tags...."
        self.remove_tags()
        print "Done."



