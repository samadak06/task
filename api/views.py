from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from .models import LuggageType, Booking
from .serializers import LuggageTypeSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import userProfileSerializer
from .models import userProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User



class CreateUserProfile(generics.CreateAPIView):
    queryset=userProfile.objects.all()
    serializer_class= userProfileSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.data:
            data = self.request.data
            data_dict = dict(data)
            username= data_dict['username']
            email = data_dict['email']
            password = data_dict['password']
            user = User.objects.create(username=username,email=email,password=password)
            serializer.save(user=user)


class userProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset=userProfile.objects.all()
    serializer_class=userProfileSerializer
    # permission_classes=[IsAuthenticated,]


class ProfilesTypeList(generics.ListAPIView):
    queryset = userProfile.objects.all()
    serializer_class = userProfileSerializer


class LuggageTypeList(generics.ListAPIView):

    queryset = LuggageType.objects.all()
    serializer_class =LuggageTypeSerializer


class LuggageTypeDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = LuggageType.objects.all()
    serializer_class = LuggageTypeSerializer



class LuggageTypeCreate(generics.CreateAPIView):
    queryset = LuggageType.objects.all()
    serializer_class = LuggageTypeSerializer


    def create(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            response = super().create(request, *args, **kwargs)
            return Response({
                'status': 200,
                'message': 'Successfully Created',
                'data': response.data
            })
        else:
            return Response({
                'message': 'You are not authorized to peform this action',

            })



class BookingTypeList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class BookingTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class BookingTypeCreate(generics.CreateAPIView):
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response({
                'message': 'Please Register With us or Login',

            })
        else:
            response = super().create(request, *args, **kwargs)
            # items = self.response.data.getlist('items')
            items = response.data.get('items')
            price = response.data.get('total_price')
            items_booked = []
            item_data = {}
            for item in items:
                item = LuggageType.objects.get(id=item)
                item_data[item.name] = item.price
            data = {
                "Name": request.user.username,
                "items": item_data,
                "Total Price": price
            }
            return Response({
                'message': 'Successfully Booked',
                'data': data
            })


    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            data = self.request.data
            data_dict = dict(data)
            items = data_dict['items']
            price = []
            for item in items:
                item = LuggageType.objects.get(id=item)
                price.append(item.price)
            serializer.save(booked_by=self.request.user,total_price=sum(price))




@login_required()
def home(request):
    return render(request,"home.html",)



def get_auth_token(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        # the password verified for the user
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            print(token.key)
            request.session['auth'] = token.key
            return redirect('/', request)
    return redirect(settings.LOGIN_REDIRECT_URL, request)

