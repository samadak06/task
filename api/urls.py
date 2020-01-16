
from django.urls import path

from . import views
from rest_framework.authtoken import views as rest_framework_views


urlpatterns = [
    #list all luggages
    path('lugagges/', views.LuggageTypeList.as_view()),

    #edit update existing luggage
    path('lugagges/<int:pk>/', views.LuggageTypeDetail.as_view()),
    #create new lugagge item, only is staff users can perform action
    path('lugagges/new-item/', views.LuggageTypeCreate.as_view()),

    #see all bookings
    path('booking/', views.BookingTypeList.as_view()),
    # path('booking/<int:pk>/', views.BookingTypeDetail.as_view()),
    #new booking all users can do booking
    path('booking/new-booking/', views.BookingTypeCreate.as_view()),

    # user signup
    path("signup/",views.CreateUserProfile.as_view(), name="signup"),
    # retrieves profile details of user
    path("profiles/<int:pk>",views.userProfileDetailView.as_view(), name="profile"),
    #see all user profiles
    path("profiles/",views.ProfilesTypeList.as_view(), name="profiles"),

]