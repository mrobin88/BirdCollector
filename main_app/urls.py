from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('birds/', views.birds_index, name='index'),
  path('birds/<int:bird_id>/', views.birds_detail, name='detail'),
  path('birds/create/', views.BirdCreate.as_view(), name='birds_create'),
  path('birds/<int:pk>/update/', views.BirdUpdate.as_view(), name='birds_update'),
  path('birds/<int:pk>/delete/', views.BirdDelete.as_view(), name='birds_delete'),
  path('birds/<int:bird_id>/add_feeding/', views.add_feeding, name='add_feeding'),
  path('birds/<int:bird_id>/add_photo/', views.add_photo, name='add_photo'),
  path('birds/<int:bird_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
  path('toys/', views.ToyList.as_view(), name='toys_index'),
  path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
  path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
  path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
  path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),
  path('accounts/signup', views.signup, name='signup'),
]                                                                                                                                                                                                                                                                                                                                                                                                                           