from notifications.models import Notification
from clients.models import Client
from transactions.models import Transaction
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth, ExtractDay, ExtractYear
from employees.models import Employee
from django.contrib.auth.models import User
import calendar
import datetime


def display_notofications(request):
    
    if 'cuser' in request.GET and request.GET['cuser'] != "":
        print(request.GET['cuser'])
        selected_employee = Employee.objects.get(id=request.GET['cuser'])
        current_user = selected_employee.user
    else: 
        current_user = request.user

    if request.user.id:
        print(current_user)
        notifications = Notification.objects.filter(receivers=request.user)
        notifications_unread = notifications.filter(receivers=request.user).filter(is_shown=False).count()


        clients = Client.objects.filter(owner=current_user)
        transactions = Transaction.objects.filter(owner=current_user)
        
        commisions_count = Transaction.objects.filter(owner=current_user).aggregate(Sum('fee'))['fee__sum']

        transactions_count = Transaction.objects.filter(owner=current_user).annotate(year=ExtractYear('timestamp'), month=ExtractMonth('timestamp')).values('month', 'year').annotate(count=Sum('fee')).values('month', 'year', 'count')
        
        employees_list = None

        transactions_all = {}
        if request.user.employee.role is 'A':
            transactions_all = Transaction.objects.all()[:10]
            employees_list = Employee.objects.all()
        
        

        return { "notifications" : notifications, "notifications_unread": notifications_unread, "clients" : clients, "transactions": transactions, "commisions_count" : commisions_count, "transactions_count" : transactions_count, "transactions_all": transactions_all, "employees_list": employees_list }
    return {}