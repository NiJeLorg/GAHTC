from registration.signals import user_activated
from django.dispatch import receiver
#for email
from django.core.mail import send_mail
from django.contrib.auth import models

@receiver(user_activated)
def send_email_to_admins(sender, **kwargs):

	group = models.Group.objects.get(name="superusers")
	users = group.user_set.all()
	useremails = []
	for u in users:
		useremails.append(u.email)

	#send email
	subject = "[GAHTC] Action required! A new user has signed up for an account."
	html_message = "Hello GAHTC Admin!<br /><br />A new user has just signed up for an account at gahtc.org. Please <a href='http://gahtc.org/admin_unverified/'>review</a> this new account and approve or reject this new applicant.<br /><br />Thank you!<br />GAHTC | Global Architectural History Teaching Collaborative"
	message = "Hello GAHTC Admin! A new user has just signed up for an account at gahtc.org. Please review this new account and approve or reject this new applicant here: http://gahtc.org/admin_unverified/ . Thank you!<br />GAHTC | Global Architectural History Teaching Collaborative"

	send_mail(subject, message, 'gahtcweb@gmail.com', useremails, fail_silently=True, html_message=html_message)

