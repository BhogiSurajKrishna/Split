from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home/$',views.home,name='home'),
    url(r'^signup/$', views.SignUp, name='signup'),
    url(r'^profile/$' , views.profile, name='profile'),
    url(r'^info/$' , views.edit_profile, name='info'),
    url(r'^friends/$', views.friends, name='friends'),
    url(r'^(?P<pk>\d+)/$', views.add_friends,name='add_friends'),
    url(r'^groups/$',views.create_group,name='create_group'),
    url(r'^add_group/$',views.add_group,name='add_group'),
    url(r'^groups/(?P<pk>\d+)/$',views.add_friends_to_group,name='add_friends_to_group'),
    # url(r'^groups/(?P<pk>\d+)/$',views.add_friends_to_group_new,name='add_friends_to_group_new'),
    url(r'^groups/(?P<pk1>\d+)/(?P<pk2>\d+)/$',views.add_friends_to_group_new,name='add_friends_to_group_new'),
    #url(r'^export/csv/$', views.export_users_csv, name='export_users_csv'),
    
]
