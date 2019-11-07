from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signup/$', views.SignUp, name='signup'),
    url(r'^profile/$' , views.profile, name='profile'),
    url(r'^info/$' , views.edit_profile, name='info'),
    url(r'^friends/$', views.friends, name='friends'),
    url(r'^(?P<pk>\d+)/$', views.add_friends,name='add_friends'),
    url(r'^groups/$',views.create_group,name='create_group'),

]
