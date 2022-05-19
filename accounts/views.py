
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product,Order,Customer
from .forms import OrderForm,CreateUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login")
    context = {"form":form}
    return render(request,'accounts/register.html',context)



def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect("/")
        else:
            messages.info(request,"Username or Password is incorrect")
            return redirect("/login")    

    context = {}
    return render(request,'accounts/login.html')    


def logout_user(request):
    logout(request)
    messages.info(request,"you are logged out")
    return redirect("/login")


@login_required(login_url="login")
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    order_count = orders.count()
    customers_count = customers.count()
    delivered = orders.filter(status="delivered").count()
    pending = orders.filter(status='pending').count()
    context = {'orders':orders,'customers':customers,
                'total_orders':order_count,'delivered':delivered,
                'pending':pending
                }
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url="login")
def products(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})


@login_required(login_url="login")
def customer(request,key):
    customer = Customer.objects.get(id=key)
    orders = customer.order_set.all()
    orders_count = orders.count()

    context = {'customer':customer,'orders':orders,'orders_count':orders_count}
    return render(request,'accounts/customer.html',context)



@login_required(login_url="login")
def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {'form':form}
    return render(request,'accounts/create_order.html',context)



@login_required(login_url="login")
def updateOrder(request,key):
    order = Order.objects.get(id=key)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {'form':form}
    return render(request,'accounts/create_order.html',context)
