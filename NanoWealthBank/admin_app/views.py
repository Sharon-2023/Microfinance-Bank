from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth, TruncDate
from customer.models import Transaction, FixedDeposit

def admin_deposits_list(request):
    deposits = FixedDeposit.objects.all().order_by('-start_date')
    context = {
        'deposits': deposits,
        'now': timezone.now()
    }
    return render(request, 'admin/admin_deposits_list.html', context)

def admin_analytics(request):
    # Get transaction data grouped by month using created_at
    transactions = Transaction.objects.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total_amount=Sum('amount'),
        transaction_count=Count('id')
    ).order_by('month')

    # Get daily transaction data
    daily_transactions = Transaction.objects.annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        daily_total=Sum('amount'),
        daily_count=Count('id')
    ).order_by('-date')[:30]  # Last 30 days

    # Format data for charts
    months = []
    amounts = []
    counts = []
    
    for transaction in transactions:
        months.append(transaction['month'].strftime('%B %Y'))
        amounts.append(float(transaction['total_amount']))
        counts.append(transaction['transaction_count'])

    # Format daily data
    dates = []
    daily_amounts = []
    daily_counts = []

    for daily in daily_transactions:
        dates.append(daily['date'].strftime('%d %b'))
        daily_amounts.append(float(daily['daily_total']))
        daily_counts.append(daily['daily_count'])

    context = {
        'months': months,
        'amounts': amounts,
        'transaction_counts': counts,
        'dates': dates,
        'daily_amounts': daily_amounts,
        'daily_counts': daily_counts,
    }
    
    return render(request, 'admin/analytics.html', context) 