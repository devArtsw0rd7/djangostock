Copyright (c) Andrew Straight 2020

from django.shortcuts import render, redirect
from .models import Stock
from django.contrib import messages
from .forms import StockForm


def index(request):
    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker']

        api_request = requests.get(
            "https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_32f0aadb11194f4dace709097a061e99")

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error"
        context = {'api': api}
        return render(request, 'stocks/index.html', context)
    else:
        context = {'ticker': 'Enter a ticker symbol above...'}
        return render(request, 'index.html', context)

    context = {'api': api}
    return render(request, 'index.html', context)


def about(request):
    context = {}
    return render(request, 'about.html', context)


def add_stock(request):
    import requests
    import json

    # Add Stock to Database
    if request.method == "POST":
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, "Stock has been added")
            return redirect('/add_stock')

    else:
        ticker = Stock.objects.all()
        # List to hold json data for each ticker_item
        output = []
        for ticker_item in ticker:

            api_request = requests.get(
                "https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_32f0aadb11194f4dace709097a061e99")

            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error"

        if ticker.exists():
            context = {'ticker': ticker, 'output': output}
            return render(request, 'add_stock.html', context)
        else:
            context = {'nodata': 'You have not added any stocks to your portfolio.'}
            return render(request, 'add_stock.html', context)


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, "Stock has been deleted!")
    return redirect('/remove_stock')


def remove_stock(request):
    ticker = Stock.objects.all()
    context = {'ticker': ticker}
    return render(request, 'remove_stock.html', context)