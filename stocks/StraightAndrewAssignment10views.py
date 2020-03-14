# Copyright (c) Andrew Straight 2020

from django.shortcuts import render, redirect
from .StraightAndrewAssignment10models import Stock
from django.contrib import messages
from .StraightAndrewAssignment10forms import StockForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate


def index(request):
    """Home page view that connects to the iexcloud API to get stock data."""
    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker']
        # Get request to the API
        api_request = requests.get(
            "https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_32f0aadb11194f4dace709097a061e99")
        # Load JSON data
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error"
        context = {'api': api}
        return render(request, 'stocks/Straight.Andrew.Assignment-10-index.html', context)
    else:
        context = {'ticker': 'Enter a ticker symbol above...'}
        return render(request, 'stocks/Straight.Andrew.Assignment-10-index.html', context)

    context = {'api': api}
    return render(request, 'Straight.Andrew.Assignment-10-index.html', context)


def about(request):
    """An about page. Not fully implemented."""
    context = {}
    return render(request, 'about.html', context)


def add_stock(request):
    """Allow user to add a stock to their portfolio. Gets current stock data via ticker symbol and
    call to the iexcloud API."""
    import requests
    import json

    # Add Stock to Database
    if request.method == "POST":
        form = StockForm(request.POST or None)
        # Form validation. If form data is valid, the data is saved and the user is informed that their stock
        # was added to the database.
        if form.is_valid():
            form.save()
            messages.success(request, "Stock has been added")
            return redirect('/add_stock')

    else:
        # Get all stock data from the database
        ticker = Stock.objects.all()
        # List to hold json data for each ticker_item
        output = []
        for ticker_item in ticker:
            # Get request to API
            api_request = requests.get(
                "https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_32f0aadb11194f4dace709097a061e99")
            # Load JSON data and append to the list for each ticker item
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error"
        # Handler- if the user has stock data, their portfolio is output and rendered to the add_stock page.
        if ticker.exists():
            context = {'ticker': ticker, 'output': output}
            return render(request, 'Straight.Andrew.Assignment-10-add_stock.html', context)
        # Otherwise, they are informed that they have not added any stocks.
        else:
            context = {'nodata': 'You have not added any stocks to your portfolio.'}
            return render(request, 'Straight.Andrew.Assignment-10-add_stock.html', context)


def delete(request, stock_id):
    """Delete a stock from the database."""
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, "Stock has been deleted!")
    return redirect('/remove_stock')


def remove_stock(request):
    """Remove stock view."""
    ticker = Stock.objects.all()
    context = {'ticker': ticker}
    return render(request, 'stocks/Straight.Andrew.Assignment-10-remove_stock.html', context)


def register(request):
    """User registration function."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        # Form validation
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
    return render(request, 'Straight.Andrew.Assignment-10-register.html', context)


def login_request(request):
    """User login function."""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        # Form validation
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
    return render(request, 'Straight.Andrew.Assignment-10-login.html', context)


def logout_request(request):
    """User logout function."""
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('stocks:index')