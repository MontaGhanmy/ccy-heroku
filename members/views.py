from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import  authenticate, login, logout
from django.views.generic import  View
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from .forms import UserForm
def index(request):
	return render(request, 'members/index.html')

'''
class UserFormss(TemplateView):
    template_name = "members/index.html"
    def get(self, request):
    	return render(request, 'members/index.html', context = {'action_type': request.GET['action_type'],})
    def post(self, request):
    	user = User.objects.create_user(request.POST['full-name'], request.POST['e-mail'], request.POST['password'])

    	return render(request, 'members/index.html', context = {'user_message': 'You just signed up to the website. Welcome !',})
'''


class UserFormView(View):
	form_class = UserForm
	template_name = "members/index.html"
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, context = {'action_type': request.GET['action_type'],'form':form,})
	def post(self, request):
		form = self.form_class(request.POST)
		if request.POST['formaction'] == 'signup':
			if form.is_valid():
				user = form.save(commit=False)
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				email = form.cleaned_data['email']
				user.set_password(password)
				user.save()
				user.userprofile.user_type = request.POST['usertype']
				user.userprofile.save()

				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
						return redirect('members:userdashboard')
					else:
						print('***Error Debug*** User not active')
				else:
					print('***Error Debug*** User is none')
			else:
				print('***Error Debug*** Form is not valid')
				print form.errors

		elif request.POST['formaction'] == 'login':
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('members:userdashboard')
		return render(request, self.template_name, context={'action_type': request.GET['action_type'], 'form': form,})

class UserDashboard(TemplateView):
	template_name = "members/dashboard.html"

def UserLogout(request):
    logout(request)
    return redirect('mainhome:index')