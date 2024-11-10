from django.shortcuts import render
from rest_framework.views import APIView
from django.views import View
from django.http import JsonResponse
from api.serializers import UserCreationSerializer
from api.serializers import CartSerializer
from api.serializers import CreatedUserSerializer
from api.serializers import ProductSerializer
from api.serializers import CartItemSerializer
from api.models import UserCreation
from api.models import CreatedUser
from api.models import Cart
from api.models import Product
from api.models import CartItem
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm


def gethome(request):
    return render(request, "store\\home.html")


def getcontact(request):
    return render(request, "store\\contact.html")


def getbase(request):
    return render(request, "store\\base.html")


def getabout(request):
    return render(request, "store\\about.html")


def getadmin(request):
    return render(request, "store\\admin.html")


def getcart(request):
    '''request.user.is_authenticated'''
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, name='stm303')
        return render(request, 'cart.html', {'cart': cart})
    else:
        return redirect('login')


def getlogin(request):
    # Check if the form has been submitted
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username and password match any entry in created_users
        try:
            user = CreatedUser.objects.get(username=username)
            if user.password == password:  # Check if password matches
                # Authenticate and log the user in
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')  # Redirect to the home page after successful login
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        except CreatedUser.DoesNotExist:
            messages.error(request, "User does not exist.")

    return render(request, 'login.html')  # Replace with your login template

def getregister(request):
    return render(request, "store\\register.html")


def getproduct(request):
    return render(request, "store\\products.html")


# returns static data, used to make sure a webpage can work
class StaticDataView(View):
    def get(self, request):
        # Define static data to return as JSON
        data = {
            'Base': {
                'title': 'Title from Base',
                'content': 'Content from the first HTML page.'
            },
            'Home': {
                'title': 'Title from Home',
                'content': 'Content from the second HTML page.'
            }
        }
        return JsonResponse(data)


# returns dynamic data from a table in the database
# viewsets.ModelViewSet handles CRUD which is needed for database output
class RegisterView(View):
    def get(self, request):
        # Display registration form
        return render(request, 'store\\register.html')

    def post(self, request):
        # Handle form submission
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Check if user already exists
        if get_user_model().objects.filter(username=username).exists():
            return HttpResponse("Username already exists", status=400)

        # Create new user
        user = get_user_model()(
            username=username,
            password=make_password(password),  # Make sure to hash the password
            email=email,
        )
        user.save()

        # Redirect to login or another page
        return redirect('login')  # Replace with your login URL


class LoginView(View):
    # Handle GET request to show the login form
    def get(self, request):
        return render(request, 'store\\login.html')  # Your login template

    # Handle POST request to check login credentials
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username and password match any entry in created_users
        try:
            user = CreatedUser.objects.get(username=username)
            if user.password == password:  # Check if password matches
                # Authenticate and log the user in
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('store\\cart')  # Redirect to the home page after successful login
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        except CreatedUser.DoesNotExist:
            messages.error(request, "User does not exist.")

        return render(request, 'store\\cart.html')


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        # Retrieve the cart for the logged-in user
        return Cart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # If a cart doesn't exist for this user, create one
        cart, created = Cart.objects.get_or_create(user=request.user)
        if created:
            return Response({"message": "Cart created."}, status=201)
        return Response({"message": "Cart already exists."})

    def add_to_cart(self, request, pk=None):
        cart = self.get_object()  # Get the cart instance for the logged-in user

        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        if not product_id or not quantity:
            return Response({"error": "Product ID and quantity are required."}, status=400)

        try:
            product = Product.objects.get(id=product_id)

        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=404)

        if quantity > product.stock_quantity:
            return Response({"error": "Not enough stock available."}, status=400)

        # Check if the product is already in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        # Update the quantity if the item already exists in the cart
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)

        # Save the cart item
        cart_item.save()

        # Update the cart's total price
        cart.save()

        return Response(CartSerializer(cart).data)

    def remove_from_cart(self, request, pk=None):
        cart = self.get_object()  # Get the cart instance for the logged-in user
        product_id = request.data.get("product_id")

        if not product_id:
            return Response({"error": "Product ID is required."}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=404)

        # Try to find the cart item
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()
            return Response({"message": "Product removed from cart."}, status=204)
        except CartItem.DoesNotExist:
            return Response({"error": "Product not in cart."}, status=404)

    def list(self, request):
        cart = self.get_queryset()
        serializer = self.get_serializer(cart, many=True)

        return Response(serializer.data)
