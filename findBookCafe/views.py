from unicodedata import name
from django.shortcuts import render
from django.http import Http404
from .models import Region, Shop, City, SimplePage
import environ
env = environ.Env()
# Create your views here.

def page404(request, exception):
	return render(request, '404.html')

def page500(exception):
	return render('404.html', exception)

def index(request):
	return render(request, 'index.html')

def findType(url_type):
	if(url_type == 'cafes'):
		return 'CAF'
	if(url_type == 'libraries'):
		return 'LIB'
	return ''

def findTemplate(url_type):
	if(url_type == 'cafes'):
		return 'cafes.html'
	if(url_type == 'libraries'):
		return 'libraries.html'
	return ''
	
def cafes(request, type):
	template = findTemplate(type)
	type = findType(type)
	if type != 'CAF' and type != 'LIB':
		raise Http404
	try:
		cafes = Shop.objects.filter(type = type)
	except:
		raise Http404
	cities = City.objects.all()
	return render(request, template, {'cafes': cafes, 'cafe_url': '/cafes', 'libraries_url': '/libraries', 'page_title': '', 'type': type, 'cities': cities})

def cafe_city(request, type, city):
	template = findTemplate(type)
	type = findType(type)
	try:
		city_find = City.objects.get(slug = city)
		regions_find = Region.objects.filter(city = city_find)
		cafes = []
		for region in regions_find:
			result = Shop.objects.filter(region=region, type = type)
			for shop in result:
				cafes.append(shop)
	except:
		raise Http404
	return render(request, template, {'cafes': cafes, 'cafe_url': '/cafes/' + city, 'libraries_url': '/libraries/' + city, 'page_title': city_find.name, 'type': type})

def cafe_region(request, type, city, region):
	template = findTemplate(type)
	type = findType(type)
	try:
		city_find = City.objects.filter(slug = city)
		region_find = Region.objects.get(slug = region, city = city_find[0])
		cafes = Shop.objects.filter(region=region_find, type = type)
	except:
		raise Http404
	return render(request, template, {'cafes': cafes, 'cafe_url': '/cafes/' + city + '/' + region, 'libraries_url': '/libraries/' + city + '/' + region, 
	'page_title': city_find[0].name + ', ' + region_find.name, 'type': type})

def cafe(request, type, city, region, cafe):
	try:
		city_find = City.objects.get(slug = city)
		region_find = Region.objects.get(slug = region, city = city_find)
		cafe_shop = Shop.objects.get(region=region_find, type = findType(type), slug=cafe)
		cafes_suggestion = Shop.objects.filter(region=region_find).order_by('?')
		cafes_suggestion = cafes_suggestion.exclude(id=cafe_shop.id)[:3]
	except:
		raise Http404
	return render(request, 'cafe.html', {'cafe': cafe_shop, 'cafes_suggestion': cafes_suggestion})

def map(request):
	shops =  Shop.objects.all()
	data = []
	for shop in shops:
		shop_type = 'Καφετέρια'
		path_type = 'cafes'
		if shop.type == 'LIB':
			shop_type = 'Βιβλιοθήκη'
			path_type = 'libraries'
		path = "/" + path_type + '/' + shop.region.city.slug + '/' + shop.region.slug
		data.append({'name': shop.name, 'slug': shop.slug, 'id': shop.id, 'directions':shop.googleMaps,  'path': path,'shopType': shop_type, 'type': "Feature", 'properties': {'iconSize': [60, 60]},
		'geometry':{'type': "Point",'coordinates': [shop.longitude, shop.latitude]}})
	return render(request, 'map.html', {'shops': data, 'map_api': env('MAP_BOX_API')})

def simple_page(request, page_slug):
	try:
		page = SimplePage.objects.get(slug = page_slug)
	except:
		raise Http404
	return render(request, 'simplePage.html', {'page_title': page.title, 'content': page.content, 'slug': page_slug})