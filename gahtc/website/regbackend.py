from registration.backends.default.views import RegistrationView
from forms import profileForm
from models import profile

class MyRegistrationView(RegistrationView):

    form_class = profileForm

    def register(self, request, form_class):
        new_user = super(MyRegistrationView, self).register(request, form_class)
        user_profile = profile.objects.get(user=new_user)
        user_profile.name = form_class.cleaned_data['name']
        user_profile.institution = form_class.cleaned_data['institution']
        user_profile.teaching = form_class.cleaned_data['teaching']
        user_profile.introduction = form_class.cleaned_data['introduction']
        user_profile.avatar = form_class.cleaned_data['avatar']
        user_profile.save()
        return user_profile