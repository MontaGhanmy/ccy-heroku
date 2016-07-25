from django.conf.urls import url
from . import views
from .views import UserFormView, UserDashboard

app_name = 'members'

urlpatterns = [
    url(r'^$', UserFormView.as_view() , name='index'),
    url(r'^dashboard/', UserDashboard.as_view() , name='userdashboard'),
    url(r'^logout/', views.UserLogout , name='userlogout'),
]
