from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Artist, Artwork, Order, Type, Basic
from datetime import datetime

# Create your views here.
def home(request):
	basic = get_object_or_404(Basic)
	artist = get_object_or_404(Artist)
	orderType = Type.objects.get(slug = 'order')
	works = Artwork.objects.exclude(types = orderType) 
	# exclude all order works
	return render(request, 'Jing/home.html', {'basic': basic, 'artist': artist, 'works': works})


def me(request):
	basic = get_object_or_404(Basic)
	artist = get_object_or_404(Artist)
	return render(request, 'Jing/home.html', {'basic': basic, 'artist': artist})

def types(request):
	basic = get_object_or_404(Basic)
	allTypes = Type.objects.exclude(slug = 'order')

	return render(request, 'Jing/types.html', {'basic': basic, 'types': allTypes})

def workType(request, slug = 'figure'):
	basic = get_object_or_404(Basic)
	workType = get_object_or_404(Type, slug = slug)
	works = get_list_or_404(Artwork, types = workType)

	return render(request, 'Jing/home.html', {'basic': basic, 'workType': workType, 'works': works})

def work(request, pk = 5):
	basic = get_object_or_404(Basic)
	artwork = get_object_or_404(Artwork, pk = pk)

	return render(request, 'Jing/home.html', {'basic': basic, 'artwork': artwork})

def purchase(request, typeSlug):
	basic = get_object_or_404(Basic)
	workType = get_object_or_404(Type, slug = typeSlug)
	if request.method == 'POST':
		form = request.POST
		# for k , v in form.items():
		# 	print(k,':',v)
		order = Order(quantity = form['quantity'], amount = form['amount'], client = form['name'], contact = form['phone'], email = form['email'], request = form['request'] ,file = form['file'])

		order.types = workType
		order.date = datetime.now()

		import hashlib
		md5 = hashlib.md5()
		md5.update((order.client+'+'+(order.date.strftime('%Y%m%d%H%M%S'))).encode('utf-8'))

		order.num = md5.hexdigest()
		order.save()

		return redirect('Jing:order', orderNum = order.num)
	return render(request, 'Jing/purchase.html', {'basic': basic, 'workType': workType})

def order(request, orderNum = 'd8313972fdc32c715b412ffd0f8b4dce'):
	basic = get_object_or_404(Basic)
	workOrder = get_object_or_404(Order, num = orderNum)

	return render(request, 'Jing/order.html', {'basic': basic, 'order': workOrder})