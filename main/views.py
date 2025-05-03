
from django.shortcuts import render, redirect, get_object_or_404
from .models import Stock, Purchase, CurrentPrice
from .forms import PurchaseForm, CurrentPriceForm
from django.db import connection
from django.db import transaction


def dashboard(request):
    # Default forms
    form = PurchaseForm()
    price_form = CurrentPriceForm()

    # Handle Purchase form submission
    if request.method == 'POST':
        if 'add_purchase' in request.POST:
            form = PurchaseForm(request.POST)
            if form.is_valid():
                with transaction.atomic():  # ✅ Transaction for data consistency
                    form.save()
                return redirect('dashboard')

        elif 'update_price' in request.POST:
            price_form = CurrentPriceForm(request.POST)
            if price_form.is_valid():
                with transaction.atomic():  # ✅ Transaction ensures price update is safe
                    stock = price_form.cleaned_data['stock']
                    CurrentPrice.objects.update_or_create(
                        stock=stock,
                        defaults={'current_price': price_form.cleaned_data['current_price']}
                    )
                return redirect('dashboard')


    # Always fetch fresh data AFTER handling forms
    prices = {cp.stock_id: cp.current_price for cp in CurrentPrice.objects.all()}
    purchases = Purchase.objects.select_related('stock').all()
    stocks = Stock.objects.all()

    data = []
    total_gain = 0

    for p in purchases:
        current_price = prices.get(p.stock_id)
        gain = None
        gain_class = ""
        if current_price:
            gain = (current_price - p.buy_price) * p.quantity
            total_gain += gain
            gain_class = "text-success" if gain >= 0 else "text-danger"
        data.append({
            'id': p.id,
            'stock_id': p.stock.id,  # ✅ Add this line
            'symbol': p.stock.symbol,
            'company': p.stock.company_name,
            'quantity': p.quantity,
            'buy_price': p.buy_price,
            'current_price': current_price,
            'gain': gain,
            'gain_class': gain_class,
        })

    return render(request, 'main/dashboard.html', {
        'form': form,
        'price_form': price_form,
        'data': data,
        'stocks': stocks,
        'total_gain': total_gain
    })



def delete_purchase(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    purchase.delete()
    return redirect('dashboard')


def edit_current_price(request, stock_id):
    stock = get_object_or_404(Stock, pk=stock_id)
    cp, _ = CurrentPrice.objects.get_or_create(stock=stock)

    if request.method == 'POST':
        form = CurrentPriceForm(request.POST, instance=cp)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CurrentPriceForm(instance=cp)

    return render(request, 'main/edit_price.html', {
        'form': form,
        'stock': stock
    })


def portfolio_report(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT s.symbol, s.company_name,
                   SUM(p.quantity) AS total_qty,
                   AVG(p.buy_price) AS avg_buy,
                   cp.current_price,
                   SUM(p.quantity) * cp.current_price - SUM(p.quantity * p.buy_price) AS gain_loss
            FROM main_purchase p
            JOIN main_stock s ON p.stock_id = s.id
            JOIN main_currentprice cp ON s.id = cp.stock_id
            GROUP BY s.id, cp.current_price
        """)
        rows = cursor.fetchall()

    return render(request, 'main/report.html', {'report_data': rows})

from django.db import connection
from django.shortcuts import render
from .models import Stock

def raw_report(request):
    results = []
    selected_symbol = None

    if request.method == 'POST':
        selected_symbol = request.POST.get('symbol')

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT s.symbol, p.quantity, p.buy_price, p.purchase_date
                FROM main_purchase p
                JOIN main_stock s ON p.stock_id = s.id
                WHERE s.symbol = %s
            """, [selected_symbol])  # ✅ Prepared statement using parameter
            results = cursor.fetchall()

    stocks = Stock.objects.all()  # For dropdown
    return render(request, 'main/raw_report.html', {
        'results': results,
        'stocks': stocks,
        'selected_symbol': selected_symbol
    })
