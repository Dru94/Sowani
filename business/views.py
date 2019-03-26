from django.shortcuts import render, get_object_or_404
from .models import Location, Suburb, Category, Business, Menu, Claim, Reviews, Reservations, Promotion, Images
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from .forms import BusinessForm, ReservationsForm, ImageForm, ReviewsForm
import requests
from django.db.models import Sum, Avg
import http.client, urllib.request, urllib.parse, urllib.error, base64
import uuid
import json
from requests.auth import HTTPBasicAuth
from django.forms import modelformset_factory
from django.contrib.auth.models import User

def claims(request, user_id, business_id):
	print ("<<<<<<<<<<................>>>>>>>>>")
	claims = Claim.objects.all()
	context = {

	}
	return render(request, 'sowani/claims.html', context )
def business(request):

    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3)
    #'extra' means the number of photos that you can upload   ^
    if request.method == 'POST':

        businessForm = BusinessForm(request.POST or None, request.FILES or None)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())


        if businessForm.is_valid() and formset.is_valid():
            business_form = businessForm.save(commit=False)
            business_form.user = request.user
            business_form.save()

            for form in formset.cleaned_data:
                #this helps to not crash if the user   
                #do not upload all the photos
                if form:
                    image = form['image']
                    photo = Images(business=business_form, image=image)
                    photo.save()
            messages.success(request,
                             "Yeeew, check it out on the home page!")
            return HttpResponseRedirect("/")
        else:
            print(businessForm.errors, formset.errors)
    else:
        businessForm = BusinessForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'sowani/business.html',
                  {'businessForm': businessForm, 'formset': formset})

def home(request):
	locations = Location.objects.all()
	categories = Category.objects.all()
	restaurants_list = []
	bars_list = []
	hotels_list = []
	restaurants = Business.objects.filter(category__name__contains="Restaurants")[:10]
	bars = Business.objects.filter(category__name__contains="Bars")[:10]
	hotels = Business.objects.filter(category__name__contains="Hotels")[:10]
	suburbs = Suburb.objects.all()
	
	for r in restaurants:
		avg_rating = Reviews.objects.filter(business=r.id).aggregate(Avg('rating'))
		number_of_reviews = Reviews.objects.filter(business=r.id).count()
		restaurants_list.append((r, avg_rating, number_of_reviews))

	for b in bars:
		avg_rating = Reviews.objects.filter(business=b.id).aggregate(Avg('rating'))
		number_of_reviews = Reviews.objects.filter(business=b.id).count()
		bars_list.append((b, avg_rating, number_of_reviews))

	for h in hotels:
		avg_rating = Reviews.objects.filter(business=h.id).aggregate(Avg('rating'))
		number_of_reviews = Reviews.objects.filter(business=h.id).count()
		hotels_list.append((h, avg_rating, number_of_reviews))

	context = {
		"locations": locations,
		"categories": categories,
		"restaurants": restaurants_list,
		"bars": bars_list,
		"hotels": hotels_list,
		"suburbs": suburbs,
	}
	return render(request, 'sowani/home.html',context)

def bars(request):
	bars = Business.objects.filter(category__name__contains="Bars")[:10]
	print ("<<<<<<<<<<<<<....... bars ......>>>>>>>>>>>>", bars)
	context = {
		'bars': bars,
	}
	return render(request, 'sowani/bars.html', context)

def hotels(request):
	hotels = Business.objects.filter(category__name__contains="Hotels")[:10]
	context = {
		'bars': hotels,
	}
	return render(request, 'sowani/bars.html', context)

def businesses_list(request, tag_slug=None):
	hotels = Business.objects.filter()
	categories = Category.objects.all()
	locations = Location.objects.all()
	suburbs = Suburb.objects.all()
	promotions = Promotion.objects.all()

	tag = None
	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		hotels = hotels.filter(tags__in=[tag])

	context = {
		'hotels': hotels,
		'categories': categories,
		'locations': locations,
		'suburbs': suburbs,
		'promotions': promotions,
		'tag': tag,
	}
	return render(request, 'sowani/hotels.html', context)

def hotel_detail(request, hotel_id, hotel_slug):
	form= ReservationsForm(request.POST or None, request.FILES or None, initial={'business': hotel_id, 'user': request.user.id})
	hotel = get_object_or_404(Business, id=hotel_id, slug=hotel_slug)
	near_by_hotels = Business.objects.filter(suburb=hotel.suburb, category=hotel.category).exclude(id=hotel_id)


	# r = requests.post('http://httpbin.org/post', json={"key": "value"})
	r = requests.post('https://ericssonbasicapi2.azure-api.net/collection/v1_0/requesttopay', json={"key": "value"})
	print("<<<<<<<<<<<<<<<<........vvvvvv.......>>>>>>>>>>>>>>>>>>", r.status_code)

	menus = Menu.objects.filter(business=hotel_id)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

	return render(request, 'sowani/hotel_detail.html', {'hotel': hotel, 'menus': menus, 
		'near_by_hotels': near_by_hotels, 'form': form})


def add_business(request):
	form= BusinessForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Business successfully added")
		return HttpResponseRedirect("/")
	return render(request, 'sowani/add_business.html', {"form": form})

def business_by_category(request, category_id, category_slug):
	businesses_list = []
	businesses = Business.objects.filter(category=category_id)
	for b in businesses:
		avg_rating = Reviews.objects.filter(business=b.id).aggregate(Avg('rating'))
		number_of_reviews = Reviews.objects.filter(business=b.id).count()
		businesses_list.append((b, avg_rating, number_of_reviews))

	category = get_object_or_404(Category, id=category_id)
	categories = Category.objects.all()
	suburbs = Suburb.objects.all()
	promotions = Promotion.objects.all()[:5]
	context = {
		'businesses': businesses_list,
		'category': category,
		'suburbs': suburbs,
		'categories': categories,
		'promotions': promotions,
	}

	return render(request, 'sowani/business_by_category.html', context)


def business_by_location(request, location_id, location_slug):
	location = get_object_or_404(Location, id=location_id)
	suburbs = Suburb.objects.filter(location=location_id)
	businesses = Business.objects.filter(location=location_id)
	categories = Category.objects.all()
	restaurants = Business.objects.filter(category__name="Restaurant")
	hotels = Business.objects.filter()
	top_bars = Business.objects.filter(category__name__contains="Bar").order_by('total_rating')[:5]
	top_restaurants = Business.objects.filter(category__name__contains="Restaurant").order_by('total_rating')[:5]
	top_cafe = Business.objects.filter(category__name__contains="Cafe").order_by('total_rating')[:5]
	top_hotels = Business.objects.filter(category__name__contains="Hotel").order_by('total_rating')[:5]
	
	context = {
		"businesses": businesses,
		"restaurants": restaurants,
		"top_bars": top_bars,
		"top_restaurants": top_restaurants,
		"top_hotels": top_hotels,
		"top_cafe": top_cafe,
		"location": location,
		"suburbs": suburbs,
		"categories": categories

	}
	return render(request, 'sowani/business_by_location.html', context)

def business_detail(request, business_id, business_slug):
	business = get_object_or_404(Business, id=business_id)
	reviews = Reviews.objects.filter(business=business_id)
	number_of_reviews = Reviews.objects.filter(business=business_id).count()
	rating_avg = Reviews.objects.filter(business=business_id).aggregate(Avg('rating'))
	promotions = Promotion.objects.filter(business=business_id)
	images = Images.objects.filter(business=business_id)
	number_of_images = Images.objects.filter(business=business_id).count()
	reviews_form= ReviewsForm(request.POST or None, request.FILES or None, initial = { 'business': business_id, 'user': request.user.id })
	if reviews_form.is_valid():
		reviews_instance = reviews_form.save(commit=False)
		reviews_instance.save()
		# messages.success(request, "Business successfully added")
		# return HttpResponseRedirect("/")

	reference_id = str(uuid.uuid4())
	collection_reference_id = str(uuid.uuid4())
	external_id = str(uuid.uuid4())
	url = 'https://ericssonbasicapi2.azure-api.net/v1_0/apiuser'
	api_key_url = 'https://ericssonbasicapi2.azure-api.net/v1_0/apiuser/'+reference_id+"/apikey"
	token_url = 'https://ericssonbasicapi2.azure-api.net/collection/token/'
	collection_url = 'https://ericssonbasicapi2.azure-api.net/collection/v1_0/requesttopay'

	avg_rating = Reviews.objects.filter(business=business_id).aggregate(Avg('rating'))	

	form= ReservationsForm(request.POST or None, request.FILES or None, initial = { 'business': business_id, 'user': request.user.id })
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

	# body = { "providerCallbackHost":"otimtony.com" }
	# response = requests.post(
 #        url, json=body, headers={'X-Reference-Id': reference_id,
 #                       'Content-Type': 'application/json; charset=UTF-8',
 #                       'Ocp-Apim-Subscription-key': 'ffefc6d52bf043a39b2930b71a6a70fc'
 #              }
 #        )

	# api_key_response = requests.post(
	# 	url=api_key_url,
	# 	params={'X-Reference-Id': reference_id},
	# 	headers={'Ocp-Apim-Subscription-key': 'ffefc6d52bf043a39b2930b71a6a70fc'}
	# 	)

	# api_key_json = json.loads(api_key_response.content)
	# api_key = api_key_json['apiKey']

	# token_response = requests.post(
	# 	url=token_url,
	# 	params={'X-Reference-Id': reference_id},
	# 	headers={'Ocp-Apim-Subscription-key': 'ffefc6d52bf043a39b2930b71a6a70fc'},
	# 	auth=HTTPBasicAuth(reference_id, api_key)
	# 	)
	# token_response_json = json.loads(token_response.content)
	# token = token_response_json['access_token']
	# collection_body = {
	# 		"amount": "10000",
	# 		"currency": "EUR",
	# 		"externalId": external_id,
	# 		"payer": { 
	# 			"partyIdType": "MSISDN", 
	# 			"partyId": "46733123453" 
	# 		},
	# 		"payerMessage": "BusinessPayment",
	# 		"payeeNote": "BusinessPayment"
	# 	}

	# collection_response = requests.post(
	# 	url=collection_url,
	# 	json = collection_body,
	# 	headers={
	# 		'Authorization': 'Bearer ' + token,
	# 		'X-Reference-Id': collection_reference_id, 
	# 		'X-Target-Environment': 'sandbox', 
	# 		'Content-Type': 'application/json; charset=UTF-8', 
	# 		'Ocp-Apim-Subscription-key': 'ffefc6d52bf043a39b2930b71a6a70fc'
	# 	},
	# )



	context = {
		'business': business,
		'reviews': reviews,
		'number_of_reviews': number_of_reviews,
		'rating_avg': rating_avg,
		'form': form,
		'avg_rating': avg_rating,
		'images': images,
		'promotions': promotions,
		"number_of_images": number_of_images,
		"reviews_form": reviews_form
	}
	return render(request, 'sowani/business_detail.html', context )

def business_by_suburb(request, suburb_id, suburb_slug):
	businesses = Business.objects.filter(suburb=suburb_id)
	suburbs = Suburb.objects.all()
	categories = Category.objects.all()
	businesses_list = []
	location = Location.objects.filter()
	for b in businesses:
		num_of_reviews = Reviews.objects.filter(business=b.id).count()
		avg_rating = Reviews.objects.filter(business=b.id).aggregate(Avg('rating'))	
		businesses_list.append((b, avg_rating, num_of_reviews))
	suburb = get_object_or_404(Suburb, id=suburb_id)

	location_id = Suburb.objects.filter(id=suburb_id)

	context = {
		"suburbs": suburbs,
		"categories": categories,
		"suburb": suburb,
		"businesses": businesses_list
	}
	return render(request, 'sowani/business_by_suburb.html', context)

def promotions_list(request):
	promotions = Promotion.objects.all()
	context = {
		'promotions': promotions,
	}
	return render(request, 'sowani/promotions_list.html', context)

def restaurants(request):
	restaurants = Business.objects.filter(category__name__contains="Restaurants")
	categories = Category.objects.all()
	locations = Location.objects.all()
	suburbs = Suburb.objects.all()
	promotions = Promotion.objects.all()
	restaurants_list = []
	for r in restaurants:
		avg_rating = Reviews.objects.filter(business=r.id).aggregate(Avg('rating'))	
		restaurants_list.append((r, avg_rating))	

	context = {
		'restaurants': restaurants,
		'categories': categories,
		'locations': locations,
		'suburbs': suburbs,
		'promotions': promotions,
		'restaurants_list': restaurants_list,
	}
	return render(request, 'sowani/restaurants.html', context)

def bars(request):
	bars = Business.objects.filter(category__name__contains="Bars")[:10]
	categories = Category.objects.all()
	locations = Location.objects.all()
	suburbs = Suburb.objects.all()
	promotions = Promotion.objects.all()
	restaurants_list = []
	for r in bars:
		avg_rating = Reviews.objects.filter(business=r.id).aggregate(Avg('rating'))	
		restaurants_list.append((r, avg_rating))

	context = {
		'bars': bars,
		'categories': categories,
		'locations': locations,
		'suburbs': suburbs,
		'promotions': promotions,
		'restaurants_list': restaurants_list,
	}
	return render(request, 'sowani/bars.html', context)

def hotels(request):
	hotels = Business.objects.filter(category__name__contains="Hotels")[:10]

	context = {
		'bars': hotels,
	}
	return render(request, 'sowani/bars.html', context)

def dashboard(request):
	reservations_list = []
	reservations = Reservations.objects.all()
	for reservation in reservations:
		user = get_object_or_404(User, id=reservation.user)
		reservations_list.append((reservation, user))
	context = {
		"reservations": reservations_list,
	}
	return render(request, 'sowani/dashboard.html', context)











