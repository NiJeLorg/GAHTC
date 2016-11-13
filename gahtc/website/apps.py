from django.apps import AppConfig

class SendEmail(AppConfig):
	name = 'website'
	
	def ready(self):
		import website.signals 