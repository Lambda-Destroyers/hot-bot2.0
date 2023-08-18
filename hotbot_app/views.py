from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
# from .forms import BotConfigForm
from .models import HotBot
from .serializer import HotBotSerializer
# from . import retrieve, training, process, main_script
from django.views.generic import CreateView, DetailView

class CustomAdminLoginView(LoginView):
    def get_success_url(self):
        if not self.request.user.is_authenticated:
            return reverse_lazy('admin:login')
        return reverse_lazy('crypto_page')

class HotBotList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = HotBot.objects.all()
    serializer_class = HotBotSerializer

# class HotBotDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = HotBot.objects.all()
#     serializer_class = HotBotSerializer

# class HotBotDetailView(DetailView):
#     model = HotBot
#     template = "transaction_detail.html"
    
class HotBotData(APIView):
    permission_classes = (IsAuthenticated,)

# def home(request):
#     form = BotConfigForm(request.POST or None)
#     if form.is_valid():
#         handle_bot_config(form)

#     # Retrieve and display the current asset positions, value, funds available, and the 24-hour chart
#     account_info = retrieve.get_account_info()
#     asset_positions = account_info  # Assuming account_info has the asset details you need
    
#     # For the 24-hour chart
#     product_id = retrieve.get_product_id('BTC', 'USD')  # Just an example
#     historical_data = retrieve.fetch_historical_data(product_id, 3600)
#     processed_data = process.process_historical_data(historical_data)
#     chart_data = training.predict_future_price(processed_data)

    # context = {
    #     'form': form,
    #     'asset_positions': asset_positions,
    #     'chart_data': chart_data,
    # }

    # return render(request, 'home.html', context)
class HomeView(CreateView):
    model = HotBot
    template_name = 'home.html'
    fields = ['owner', 'price', 'currency', 'bot_run_time', 'desired_ROI', 'stop_loss']


def handle_bot_config(form):
    price = form.cleaned_data['price']
    currency = form.cleaned_data['currency']
    bot_run_time = form.cleaned_data['bot_run_time']
    desired_ROI = form.cleaned_data['desired_ROI']
    stop_loss = form.cleaned_data['stop_loss']
    
    # Set the amount to trade to the specified price, and set the order type to "limit"
    amount_to_trade = price
    order_type = "limit"
    
    # Call the trade_crypto function with the parameters from the form
    response = main_script.trade_crypto(currency, 'USD', amount_to_trade, 'buy', order_type, price)
    
    # You can handle the response as needed, such as printing it or logging it
    print(response)

