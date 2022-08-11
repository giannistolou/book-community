from django.shortcuts import render
from .models import Shop
import environ
env = environ.Env()
# Create your views here.
def index(request):
	return render(request, 'index.html')

def cafes(request):
	cafes = Shop.objects.filter(type = 'CAF')
	return render(request, 'cafes.html', {'cafes': cafes})

def cafe(request, cafe):
	id = cafe.split('-')[-1]
	cafe = Shop.objects.get(id=id)
	return render(request, 'cafe.html', {'cafe': cafe})
	
def libraries(request):
	libraries = Shop.objects.filter(type = 'LIB')
	return render(request, 'libraries.html', {'cafes': libraries})

def map(request):
	shops =  Shop.objects.all()
	data = []
	for shop in shops:
		shop_type = 'Καφετέρια'
		if shop.type == 'LIB':
			shop_type = 'Βιβλιοθήκη'
		data.append({'name': shop.name, 'id': shop.id, 'directions':shop.googleMaps,  'shopType': shop_type, 'type': "Feature", 'properties': {'iconSize': [60, 60]},
		'geometry':{'type': "Point",'coordinates': [shop.longitude, shop.latitude]}})
	return render(request, 'map.html', {'shops': data, 'map_api': env('MAP_BOX_API')})