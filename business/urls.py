from django.conf.urls import url
# from django.contrib.auth.views import login
from . import views

app_name='business'

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^add_business/$', views.add_business, name='add_business'),
	url(r'^business/$', views.business, name='business'),
	url(r'^claims/(?P<user_id>\d+)/(?P<business_id>\d+)$', views.claims, name='claims'),
	url(r'^hostels/$', views.businesses_list, name='businesses_list'),
	url(r'^promotions/$', views.promotions_list, name='promotions_list'),
	url(r'^suburb/(?P<suburb_id>\d+)/(?P<suburb_slug>[-\w]+)/$', views.business_by_suburb, name='business_by_suburb'),
	url(r'^(?P<location_id>\d+)/(?P<location_slug>[-\w]+)/$', views.business_by_location, name='business_by_location'),
	url(r'^detail/(?P<business_id>\d+)/(?P<business_slug>[-\w]+)/$', views.business_detail, name='business_detail'),
	# url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.businesses_list, name='businesses_list_by_tag'),
	url(r'^restaurants/$', views.restaurants, name='restaurants'),
	url(r'^hotels/$', views.hotels, name='hotels'),
	url(r'^dashboard/$', views.dashboard, name='dashboard'),
	url(r'^bars/$', views.bars, name='bars'),
	url(r'^category/(?P<category_id>\d+)/(?P<category_slug>[-\w]+)/$', views.business_by_category, name='business_by_category'),
	url(r'^(?P<hotel_id>\d+)/(?P<hotel_slug>[-\w]+)/$', views.hotel_detail, name='hotel_detail'),

]


