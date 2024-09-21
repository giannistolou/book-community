from cProfile import label
from random import choices
from django.db import models
from django_quill.fields import QuillField

# Create your models here.

CAFE_TYPES_OPTIONS = [
        ('CAF', 'Καφετέρια'),
        ('LIB', 'Βιβλιοθήκη'),
      ]

INTERNET_CHOICE = [
	('0', 'none'),
	('1', 'bad'),
	('2', 'normal'),
	('3', 'good')
]

POWER_OUTLETS_CHOICE = [
	('0', 'none'),
	('1', 'few'),
	('2', 'normal'),
	('3', 'many'),
	('4', 'is everywhere')
]

class City(models.Model):
	name = models.CharField(max_length=200, primary_key=True)
	name_en = models.CharField(max_length=200, default=name)
	slug= models.CharField(max_length=200, default=name_en)

class Region(models.Model):
	city = models.ForeignKey(City, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, primary_key=True)
	name_en = models.CharField(max_length=200, default=name)
	slug= models.CharField(max_length=200, default=name_en)

class Shop(models.Model):
	id = models.AutoField(primary_key=True, editable=False)
	type = models.CharField(choices=CAFE_TYPES_OPTIONS, max_length=3, default=CAFE_TYPES_OPTIONS[0])
	thumbnail = models.ImageField(upload_to ='uploads/', null = True)
	name = models.CharField(max_length=300)
	name_en = models.CharField(max_length=300, default= name)
	slug = models.CharField(max_length=300, default= name_en)
	latitude = models.FloatField(max_length=100)
	longitude = models.FloatField(max_length=100)
	address = models.CharField(max_length=300)
	region = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL)
	website = models.URLField(max_length=300, blank=True)
	facebook = models.URLField(max_length=300, blank=True)
	instagram = models.URLField(max_length=300, blank=True)
	tripadvisor = models.URLField(max_length=300, blank=True)
	googleMaps = models.URLField(max_length=300, blank=True)
	isBookShop = models.BooleanField()
	isAccessibleForPeopleWithDisabilities = models.BooleanField(default=False)
	isCoffeeAllowed = models.BooleanField(default=True)
	hasLunch = models.BooleanField(default=False)
	internetQuality = models.CharField(choices=INTERNET_CHOICE, max_length=1, default=INTERNET_CHOICE[2])
	powerOutlets = models.CharField(choices=POWER_OUTLETS_CHOICE, max_length=1, default=POWER_OUTLETS_CHOICE[2])
	description = QuillField()
	created_date = models.DateField(auto_now_add = True)
	updated_on = models.DateField(auto_now= True)
	order_position = models.IntegerField(default=0)
	
	def __str__(self):
		return str(self.id) + ' ' + self.name + ' ' + self.type

class SimplePage(models.Model):
	id = models.AutoField(primary_key=True, editable=False)
	title = models.CharField(max_length=500, unique=True)
	slug = models.CharField(max_length=300, unique=True)
	content = QuillField()
	created_date = models.DateField(auto_now_add = True)
	updated_on = models.DateField(auto_now= True)

	def __str__(self):
		return str(self.title)

class Collection(models.Model):
	id = models.AutoField(primary_key=True, editable=False)
	title = models.CharField(max_length=500)
	description = models.CharField(max_length=160)
	slug = models.CharField(max_length=300, unique=True)
	created_date = models.DateField(auto_now_add = True)
	updated_on = models.DateField(auto_now= True)
	thumbnail = models.ImageField(upload_to ='uploads/', null = True)
	shops = models.ManyToManyField(Shop)
	order_position = models.IntegerField(default=0)
	
	def __str__(self):
		return str(self.title)