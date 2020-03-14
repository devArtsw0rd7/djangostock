# Copyright (c) Andrew Straight 2020

from django.shortcuts import render, redirect
from .models import Stock
from django.contrib import messages
from .forms import StockForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate


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


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")
            return redirect('stocks:index')
        else:
            for message in form.error_messages:
                messages.error(request, f"{message}:{form.error_messages[message]}")
    form = UserCreationForm
    context = {'form': form}
    return render(request, 'register.html', context)


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('stocks:add_stock')
            else:
                return messages.error(request, 'Invalid username or password')
        else:
            return messages.error(request, 'Invalid username or password')
    form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'login.html', context)


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('stocks:index')