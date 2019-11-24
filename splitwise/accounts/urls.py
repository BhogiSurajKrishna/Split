from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home/$',views.home,name='home'),
    url(r'^signup/$', views.SignUp, name='signup'),
    url(r'^activity/$', views.activity, name='Activity'),
    url(r'^profile/$' , views.profile, name='profile'),
    url(r'^info/$' , views.edit_profile, name='info'),
    url(r'^friends/$', views.friends, name='friends'),
    url(r'^ulfa/(?P<pk>\d+)/$', views.add_friends,name='add_friends'),
    url(r'^friends/(?P<pk>\d+)/$', views.friend_detail,name='friend_detail'),
    url(r'^groups/$',views.create_group,name='create_group'),
    url(r'^trans/(?P<pk>\d+)/$',views.new_trans,name='new_trans'),
    url(r'^settle/(?P<pk>\d+)/(?P<pk1>\d+)/(?P<pk2>\d+)/$',views.settle,name='settle'),
    url(r'^add_group/$',views.add_group,name='add_group'),
    url(r'^groups/(?P<pk>\d+)/$',views.add_friends_to_group,name='add_friends_to_group'),
    # url(r'^groups/(?P<pk>\d+)/$',views.add_friends_to_group_new,name='add_friends_to_group_new'),
    url(r'^groups/(?P<pk1>\d+)/(?P<pk2>\d+)/$',views.add_friends_to_group_new,name='add_friends_to_group_new'),
    url(r'^edit_trans/(?P<pk>\d+)/(?P<pk1>\d+)/$',views.edit_trans,name='edit_trans'),
    url(r'^SettleUp/$', views.settleup, name='Settleup'),
    url(r'^balances/(?P<pk>\d+)/$' , views.show_balances, name='show_balances'),
       
]
