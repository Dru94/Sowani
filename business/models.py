from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class Location(models.Model):
	name = models.CharField(max_length=200, db_index=True)
	image = models.ImageField(upload_to='location/%Y/%m/%d',blank=True)
	slug = models.SlugField(max_length=200, db_index=True, unique=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'location'
		verbose_name_plural = 'locations'
		
	def __str__(self):	
		return self.name

class Suburb(models.Model):
	location = models.ForeignKey(Location, related_name='suburb', on_delete=models.CASCADE)
	name = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(max_length=200, db_index=True, unique=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'suburb'
		verbose_name_plural = 'suburbs'
		
	def __str__(self):	
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=200, db_index=True)
	image = models.ImageField(upload_to='category/%Y/%m/%d',blank=True)
	slug = models.SlugField(max_length=200, db_index=True, unique=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'
		
	def __str__(self):	
		return self.name

class Business(models.Model):
	location = models.ForeignKey(Location, related_name='business_locations', on_delete=models.CASCADE)
	suburb = models.ForeignKey(Suburb, related_name='business_suburbs', on_delete=models.CASCADE)
	category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE)
	slogan = models.CharField(max_length=200, db_index=True)
	name = models.CharField(max_length=200, db_index=True)
	phone = models.CharField(max_length=200, db_index=True)
	email = models.EmailField()
	total_rating = models.PositiveIntegerField(null=True)
	photos = models.ImageField(upload_to='business_photos/%Y/%m/%d',blank=True)
	slug = models.SlugField(max_length=200, db_index=True, unique=True)
	description = models.TextField()
	tags = TaggableManager()
	openTime = models.TimeField()
	closeTime = models.TimeField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'business'
		verbose_name_plural = 'businesses'
		
	def __str__(self):	
		return self.name

	def get_absolute_url(self):
		return reverse('business:business_detail', args=[self.id, self.slug])

def get_image_filename(instance, filename):
    name = instance.business.name
    slug = slugify(name)
    return "business_images/%s-%s" % (slug, filename)  


class Images(models.Model):
    business = models.ForeignKey(Business, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='Image')

def create_slug(instance, new_slug=None):
	slug = slugify(instance.name)
	if new_slug is not None:
		slug  = new_slug
	qs = Business.objects.filter(slug=slug).order_by("-id")
	exists= qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Business)

class Menu(models.Model):
	business = models.ForeignKey(Business, related_name='business_menus', on_delete=models.CASCADE)
	photos = models.ImageField(upload_to='menu_photos/%Y/%m/%d',blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('business',)
		verbose_name = 'menu'
		verbose_name_plural = 'menus'
		
	# def __str__(self):	
	# 	return self.business

class Reviews(models.Model):
	RATING_CHOICES = ((1, 'one'), (2, 'two'), (3, 'three'), (4, 'four'), (5, 'five'))
	user = models.PositiveIntegerField(null=True)
	business = models.ForeignKey(Business, related_name='business', on_delete=models.CASCADE, null=True)
	rating = models.PositiveSmallIntegerField('Rate', blank=False, default=3, choices=RATING_CHOICES)
	images = models.ImageField(upload_to='rating_photos/%Y/%m/%d',blank=True, null=True)
	comment = models.TextField(null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('business',)
		verbose_name = 'rating'
		verbose_name_plural = 'ratings'
		
	def __str__(self):	
		return str(self.business)

class Reservations(models.Model):
	TIME_CHOICES = (
		('5:00 AM', '5:00 AM'), ('5:30 AM', '5:30 AM'), 
		('6:00 AM', '6:00 AM'), ('6:30 AM', '6:30 AM'), 
		('7:00 AM', '7:00 AM'), ('7:30 AM', '7:30 AM'), 
		('8:00 AM', '8:00 AM'), ('8:30 AM', '8:30 AM'), 
		('9:00 AM', '9:00 AM'), ('9:30 AM', '9:30 AM'), 
		('10:00 AM', '10:00 AM'), ('10:30 AM', '10:30 AM'), 
		('11:00 AM', '11:00 AM'), ('11:30 AM', '11:30 AM'), 
		('12:00 PM', '12:00 PM'), ('12:30 PM', '12:30 PM'), 
		('1:00 PM', '1:00 PM'), ('1:30 PM', '1:30 PM'), 
		('2:00 PM', '2:00 PM'), ('2:30 PM', '2:30 PM'), 
		('3:00 PM', '3:00 PM'), ('3:30 PM', '3:30 PM'), 
		('4:00 PM', '4:00 PM'), ('4:30 PM', '4:30 PM'), 
		('5:00 PM', '5:00 PM'), ('5:30 PM', '5:30 PM'), 
		('6:00 PM', '6:00 PM'), ('6:30 PM', '6:30 PM'), 
		('7:00 PM', '7:00 PM'), ('7:30 PM', '7:30 PM'), 
		('8:00 PM', '8:00 PM'), ('8:30 PM', '8:30 PM'), 
		('9:00 PM', '9:00 PM'), ('9:30 PM', '9:30 PM'), 
		('10:00 PM', '10:00 PM'), ('10:30 PM', '10:30 PM'), 
		('11:00 PM', '11:00 PM'), ('11:30 PM', '11:30 PM'), 
		('12:00 PM', '12:00 PM'))
	business = models.PositiveIntegerField()
	user = models.PositiveIntegerField()
	amount = models.PositiveIntegerField(default="0")
	people = models.PositiveIntegerField()
	date = models.DateField()
	time = models.CharField(max_length=10, blank=False, default='8:00 AM', choices=TIME_CHOICES)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('business',)
		verbose_name = 'reservation'
		verbose_name_plural = 'reservations'
		
	def __str__(self):	
		return str(self.business)

class Promotion(models.Model):
	business = models.ForeignKey(Business, related_name='business_promotions', on_delete=models.CASCADE)
	name = models.CharField(max_length=200, db_index=True)
	number_of_reservations = models.PositiveIntegerField()
	images = models.ImageField(upload_to='promotions/%Y/%m/%d',blank=True)
	slug = models.SlugField(max_length=200, db_index=True, unique=True)
	description = models.TextField()
	startDate = models.DateField()
	endDate = models.DateField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('business',)
		verbose_name = 'promotion'
		verbose_name_plural = 'promotions'
		
	def __str__(self):	
		return self.name

class Claim(models.Model):
	user = models.PositiveIntegerField(null=True)
	business = models.PositiveIntegerField(null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-created',)
		verbose_name = 'claim'
		verbose_name_plural = 'claims'
		
	def __str__(self):	
		return str(self.business)












