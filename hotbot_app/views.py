from django.http import request
from rest_framework import generics
from .serializer import HotBotSerializer
from .models import HotBot
from rest_framework.permissions import IsAuthenticated
from .permissions import isOwnerOrReadOnly
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomAdminLoginView(LoginView):
    def get_success_url(self, request):
        # Redirect to the desired page after successful login
        # return reverse_lazy('http://127.0.0.1:8000/crypto-page')
      if not request.user.is_authenticated:
        return redirect('/admin/login/?next=/')

      return render(request, 'http://127.0.0.1:8000/crypto-page')

    # def form_valid(self, form):
    #     if self.request.user.is_superuser:
    #         return super().form_valid(form)
    #     else:
    #         return redirect('admin:login') 

class HotBotList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = HotBot.objects.all()
    serializer_class = HotBotSerializer


class HotBotDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = HotBot.objects.all()
    serializer_class = HotBotSerializer


# Create your views here.

