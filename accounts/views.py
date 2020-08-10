from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm, MenuForm
from django.forms import inlineformset_factory
from django.core.paginator import Paginator
from .filters import OrderFilter, MenuFilter
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    last_5_orders = orders.order_by('-date_created')[:5]
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders, 'customers': customers, 'total_customers': total_customers,
               'total_orders': total_orders, 'delivered': delivered, 'pending': pending, 'last_5_orders': last_5_orders}
    return render(request, 'accounts/dashboard.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'total_orders':total_orders,
               'delivered':delivered,'pending':pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customers = Customer.objects.get(id=pk_test)
    orders = customers.order_set.all()
    orders_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'customers': customers, 'orders': orders, 'orders_count': orders_count, 'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)


######## MENUS CRUD VIEWS ########
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def menus(request):
    menus = Menu.objects.all().order_by('date_created')
    myFilter = MenuFilter(request.GET, queryset=Menu.objects.all())
    menus = myFilter.qs
    paginator = Paginator(menus, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'menus': menus, 'page_obj': page_obj, 'myFilter': myFilter}
    return render(request, 'accounts/menus.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_menu(request):
    form = MenuForm()
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'The menu has been created successfully!')
            return redirect('menus')

    context = {'form': form}
    return render(request, 'accounts/create_menu.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_menu(request, pk):
    menu = Menu.objects.get(id=pk)
    form = MenuForm(instance=menu)
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            messages.info(request, 'The menu has been successfully updated!')
            return redirect('menus')
    context = {'form': form}
    return render(request, 'accounts/create_menu.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_menu(request, pk):
    menu = Menu.objects.get(id=pk)
    if request.method == 'POST':
        menu.delete()
        messages.warning(request, 'The menu has been successfully deleted!')
        return redirect('menus')
    context = {'menu': menu}
    return render(request, 'accounts/menus.html', context)

######## ORDERS CRUD VIEWS ########
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('menu', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'order': order}
    return render(request, 'accounts/dashboard.html', context)


######## STATISTICS VIEW ########
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def stats(request):
    labels = []
    data = []

    labels1 = []
    data1 = []

    orders_by_month = Order.objects.annotate(month=TruncMonth('date_created')).values('month').annotate(c=Count('id')).values_list('month', 'c')
    revenue_by_month = Order.objects.annotate(month=TruncMonth('date_created')).values('month').annotate(total=Sum('menu__price')).values_list('month', 'total')

    for i in orders_by_month:
            labels.append(i[0])
            data.append(i[1])

    for i in revenue_by_month:
            labels1.append(i[0])
            data1.append(i[1])

    context = {'labels': labels,'data': data, 'labels1': labels1,'data1': data1}
    return render(request, 'accounts/stats.html', context)


