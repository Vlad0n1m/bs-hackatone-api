from django.urls import path
from .views import ProfileUpdateView, ProfileDetailView, ProfileListView, UserProfileView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('', ProfileListView.as_view(), name='profile-list'),
    path('update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('<str:username>/', ProfileDetailView.as_view(), name='profile-detail'),

]