from django.urls import path

from . import views

urlpatterns = [
    path('blocking', views.blocking, name='blocking'),
    path('background', views.background, name='background'),
    path('async_with_block', views.async_with_block, name='async_with_block'),
    path('async_no_block', views.async_no_block, name='async_no_block'),
]