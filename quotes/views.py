from django.shortcuts import render, redirect
from .models import Stock
from django.contrib import messages
from .forms import StockForm

# Create your views here.

def home(request):
	import requests
	import json

	if request.method == 'POST':

		ticker = request.POST['ticker']
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_b36d0a77ca4149f2a03c580073768523")
		#api_request = requests.get("https://cloud.iexapis.com/stable/stock/aapl/quote?token=pk_b36d0a77ca4149f2a03c580073768523")

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."
		
		return render(request, 'home.html', {'api': api})

	else:
		return render(request, 'home.html', {'ticker': "Enter a Ticker Symbol Above."})

	# API Key - pk_b36d0a77ca4149f2a03c580073768523

	#return render(request, 'home.html', {'api': api})

def about(request):
	return render(request, 'about.html', {})

def add_stock(request):
	import requests
	import json

	if request.method == 'POST':
		#ticker = request.POST['ticker']
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock has been added!"))
			return redirect('add_stock')

	else:

		ticker = Stock.objects.all()
		output = []

		for ticker_item in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_b36d0a77ca4149f2a03c580073768523")

			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error..."

		return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})

def delete(request, stock_id):

	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock has been deleted."))
	return redirect(delete_stock)

def delete_stock(request):

	ticker = Stock.objects.all()

	return render(request, 'delete_stock.html', {'ticker': ticker})






