from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import (
    UpdateView,
    DeleteView,
    CreateView,
    DetailView,
)

def index(request):
    products = Product.objects.order_by('-id')[:4]
    context =  {'products':products,'top':'-top', 'header':'header-transparent'}
    return render(request, 'hoard/index.html', context)

def checkout(request):
    context = {}
    return render(request, 'hoard/checkout.html', context)
def store(request):
    products = Product.objects.all()
    customer, created = Customer.objects.get_or_create(user = request.user)
    try:
        order = Order.objects.get(customer=customer)
        context =  {'products':products, 'cartItems': order.cart_items()}
    except ObjectDoesNotExist:
        order = None
        context =  {'products':products}
    return render(request, 'hoard/store.html', context)

def cart(request):
    if  request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user = request.user)
        order, created = Order.objects.get_or_create(customer=customer)
        context = {'order': order,'total':order.get_total(), 'cartItems': order.cart_items()}
    return render(request, 'hoard/cart.html',context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            uservalue = form.cleaned_data.get('username')
            messages.success(request,'Account Created')
            return redirect('home')
        else:
            messages.warning(request,'ERROR !')
    else:
        form = UserRegisterForm()
    return render(request, 'hoard/register.html', {'form':form})

class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title','type', 'price','description', 'image']

    def form_valid(self, form):
        print(self.request.POST)
        owner , created = Owner.objects.get_or_create(user=self.request.user)
        form.instance.owner = self.request.user.owner
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['title','type', 'price','description', 'image']

    def form_valid(self, form):
        form.instance.owner = self.request.user.owner
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user.owner == product.owner:
            return True
        return False


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'

    def test_func(self):
        product = self.get_object()
        if self.request.user.owner == product.owner:
            return True
        return False

def updateItem(request):
    productID = request.POST.get('productID')
    action = request.POST.get('action')
    customer = request.user.customer
    print(action)
    print(productID)
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=customer, complete = False)

    if action=='add':
        order.products.add(product)
    elif action=='remove':
        order.products.remove(product)
    order.save()

    if not order.products:
        order.delete()

    context={'cartItems': order.cart_items(),'order':order}
    if request.is_ajax:
        cart_html= render_to_string('hoard/cart_product.html', context , request=request)
        html= render_to_string('hoard/cart_var.html', context , request=request)
        context = { 'form': html, 'cart':cart_html }
        return JsonResponse(context)
