from django.db import models
from django.urls import reverse

# Create your models here.
class Artist(models.Model):
	"""author, painter, photographer, coder"""
	name = models.CharField(max_length = 32, help_text = 'nickname')
	label = models.CharField(max_length = 150, help_text = 'brief introduction, lable etc.')
	intro = models.TextField(help_text = 'introduce yourself')
	avatar = models.FileField(upload_to = 'Jing/author/', null = True, blank = True)

	def __str__(self):
		return '{}:{}'.format(self.name, self.label)

	def get_absolute_url(self):
		return reverse('Jing:me')


def type_path(instance, filename):
	'path to save type file'
	return 'Jing/{}/{}'.format(instance.name, filename)

class Type(models.Model):
	"""
	page for show the work type, include introduction and purchase
	"""
	name = models.CharField(max_length = 32, help_text = "how you call it?")
	slug = models.SlugField('the English name', max_length = 32)
	intro = models.TextField(help_text = 'what type is it, describe it')
	price = models.PositiveSmallIntegerField(default = 0, null = True, blank = True, help_text = 'single price for this type of work')
	demo = models.FileField(upload_to = type_path, null = True, blank = True) 

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('Jing:workType', kwargs={'slug': self.slug})


def work_path(instance, filename):
	'path to save artwork'
	return 'Jing/{}/{}'.format(instance.types.name, filename)

class Artwork(models.Model):
	'''
	ervery work, for show, order's work is also here, but should in order types for not appear
	'''
	name = models.CharField(max_length = 32, blank = False, help_text = 'the name of this work')
	intro = models.TextField(help_text = 'how it was created and what were you thinking when you make it')
	date = models.DateField(auto_now = True, help_text = 'uploaded date')
	types = models.ForeignKey(Type, models.SET_NULL, null = True, blank = True)
	file = models.FileField(upload_to = work_path)

	def __str__(self):
		return '{} | {}'.format(self.name, self.types.name)

	def get_absolute_url(self):
		return reverse('Jing:work', kwargs={'pk': self.pk})



class Order(models.Model):
	'''
	order pruduct, slug url show every order, also works will belong here
	'''
	num = models.SlugField(max_length = 32)
	types = models.ForeignKey(Type, models.SET_NULL, null = True, blank = True)
	quantity = models.PositiveSmallIntegerField(default = 1, null = False, blank = False)
	amount = models.PositiveIntegerField(null = False, blank = False, help_text = 'total amount of the order') 
	date = models.DateTimeField(help_text = 'date time of purchase')

	client = models.CharField(max_length = 32, help_text = 'the name of the client')
	email = models.EmailField(max_length = 50, null = True, blank = True, help_text = 'the email address ') 
	contact = models.CharField(max_length = 50, help_text = 'phone number, QQ, wechat etc for contact', null = True, blank = True)
	request = models.TextField(help_text = 'write your requirements here')
	file = models.FileField(upload_to = 'Jing/order/', blank = True, null = True)

	orderStatus = (
		('waiting', '已加入创作队列'),
		('processing', '正在创作中'),
		('completed', '创作已完成'),
		)

	state = models.CharField(max_length = 10, choices = orderStatus, default = 'waiting')
	note = models.TextField(help_text = 'author\'s order remarks', null=True, blank = True)
	works = models.ForeignKey(Artwork, models.SET_NULL, null = True, blank = True)

	def __str__(self):
		return '{}:{} | {}元'.format(self.client, self.types.name, self.amount)

	def get_absolute_url(self):
		import hashlib
		md5 = hashlib.md5()
		od = self.date.strftime('%Y%m%d%H%M%S')
		md5.update((self.client+'+'+od).encode('utf-8'))

		return reverse('Jing:order', args = [md5.hexdigest()])


class Basic(models.Model):
	title = models.CharField(max_length = 32)
	showWorks = models.CharField(max_length = 32)
	showTypes = models.CharField(max_length = 32)
	orderButton = models.CharField(max_length = 10)