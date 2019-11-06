from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signup/', views.SignUp, name='signup'),
    url(r'^profile/' , views.profile, name='profile'),
    url(r'^info/' , views.edit_profile, name='info'),
    
]
