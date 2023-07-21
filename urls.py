from django.urls import path
from . import views

app_name = "Jing"
urlpatterns = [
	path('', views.home, name = "home"),
	path('me/', views.me, name = "me"),
	path('types/', views.types, name = 'types'),
	path('type', views.workType, name = 'defaultType'),
	path('type/<slug:slug>', views.workType, name = 'workType'),
	path('work/', views.work, name = "defaultWork"),
	path('work/<int:pk>', views.work, name = "work"),
	path('purchase/<slug:typeSlug>', views.purchase, name = "purchase"),
	path('order/', views.order, name = "defaultOrder"),
	path('order/<str:orderNum>', views.order, name = 'order')

]