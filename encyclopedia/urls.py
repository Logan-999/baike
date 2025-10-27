from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'entries', views.EntryViewSet, basename='entry')
router.register(r'favorites', views.FavoriteViewSet, basename='favorite')
router.register(r'search', views.SearchViewSet, basename='search')

urlpatterns = [
    path('', include(router.urls)),
    path('encyclopedia/statistics/', views.StatisticsView.as_view(), name='statistics'),
]