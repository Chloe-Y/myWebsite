from django.test import TestCase
from django.shortcuts import reverse
from Jing.models import Basic, Artist, Artwork, Type, Order

def create_basic():
	return Basic.objects.create(title = 'test title', showWorks = 'test showWorks', showTypes = 'test showTypes', orderButton = 'test show orderButton')

def create_more_basic():
	b1 = Basic.objects.create(title = 'test title', showWorks = 'test showWorks', showTypes = 'test showTypes', orderButton = 'test show orderButton')
	b2 = Basic.objects.create(title = 'test 2 title', showWorks = 'test 2 showWorks', showTypes = 'test 2 showTypes', orderButton = 'test 2 show orderButton')

	return 'False, created more than 1 basic'

def create_artist():
	return Artist.objects.create(name = 'test', label = 'test label', intro = 'test intro',avatar = './static/test.jpg')

def create_more_artist():
	a1 = Artist.objects.create(name = 'test', label = 'test label', intro = 'test intro', avatar = './static/test.jpg')
	a2 = Artist.objects.create(name = 'test more', label = 'test more label', intro = 'test more intro', avatar = './static/test.jpg')
	return 'False, created more than 1 artist'

def create_types_without_order():
	t1 = Type(name = 'type 1', slug = 'type1', intro = 'test type 1', demo = './static/test.jpg')
	t2 = Type(name = 'type 2', slug = 'type2', intro = 'test type 2', demo = './static/test.jpg')
	t1.save()
	t2.save()
	return 'created 2 types without type order'

def create_types_with_order():
	t1 = Type(name = 'type 1', slug = 'type1', intro = 'test type 1', demo = './static/test.jpg')
	t2 = Type(name = 'type 2', slug = 'type2', intro = 'test type 2', demo = './static/test.jpg')
	tOrder = Type(name = 'order type', slug = 'order', intro = 'test order type', demo = './static/test.jpg')

	t1.save()
	t2.save()
	tOrder.save()
	return 'created 2 types with type order'	

# Create your tests here.
class JingTests(TestCase):
	def test_index_view_without_objects(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 404)

	def test_index_view_with_objects(self):
		create_artist()
		create_basic()
		create_types_with_order()

		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)


	def test_more_than_1_artist_view(self):
		create_basic()
		create_more_artist()

		artistNum = Artist.objects.all().count()

		self.assertEqual(artistNum, 2)


	def test_more_than_1_basic_view(self):
		create_more_basic()
		create_artist()

		basicNum = Basic.objects.all().count()

		self.assertEqual(basicNum, 2)


	def test_no_order_type_view(self):
		create_basic()
		create_types_without_order()

		typeNum = Type.objects.all().count()
		self.assertEqual(typeNum, 2)

		response = self.client.get(reverse('Jing:types'))
		self.assertEqual(response.status_code, 200)


	def test_with_order_type_view(self):
		create_basic()
		create_types_with_order()

		response = self.client.get(reverse('Jing:types'))
		t1 = Type.objects.get(slug = 'type1')
		t2 = Type.objects.get(slug = 'type2')
		self.assertQuerysetEqual(response.context['types'].order_by('name'), [t1, t2])
