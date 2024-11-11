from django.shortcuts import render
from rest_framework.views import APIView
from django.views import View
from django.http import JsonResponse
from api.serializers import UserSerializer
from api.serializers import CartSerializer
from api.serializers import OrderSerializer
from api.serializers import OrderDetailsSerializer
from api.serializers import ShippingDetailsSerializer
from api.serializers import CartItemSerializer
from api.models import User, StoreStock, Cart, Order, OrderDetails, ShippingInformation, CartItem
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import logout

def getlogout(request):
    logout(request)  # Logs out the current user
    return redirect('login')

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


'''def getlogin(request):
    # Check if the form has been submitted
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username and password match any entry in created_users
        try:
            user = .objects.get(username=username)
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

    return render(request, 'login.html')  # Replace with your login template'''

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
    def get(self, request):
        # Render the login page when the user navigates to the login page
        return render(request, 'store/login.html')

    def post(self, request):
        # Get the username and password from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Debugging output to check if the data is being passed correctly
        print(f"Attempting to log in with username: {username} and password: {password}")

        try:
            # Retrieve the user from the 'created_users' table by username
            user = User.objects.get(username=username)

            # Debugging output to check if the user is retrieved
            print(f"User found: {user}")
            print(f"Password: {user.password}")
            print(f"Input: {password}")
            # Check if the provided password matches the hashed password in the database
            if user.password == password:  # Use user.check_password() for hashed passwords
                print("Password is correct. Attempting to authenticate.")
                #user = authenticate(request, username=username, password=password)
                #request.session['user_id'] = user.id
                login(request, user)
                return redirect('cart')
                '''if user is not None:
                    print("Authentication successful.")
                    login(request, user)
                    return redirect('store/cart.html')  # Redirect to the user's home page or cart page after successful login
                else:
                    print("Authentication failed.")
                    messages.error(request, "Invalid username or password.")'''
            else:
                print("Password mismatch.")
                messages.error(request, "Invalid username or password.")
        except User.DoesNotExist:
            # Handle the case where the user doesn't exist in the database
            print("User does not exist.")
            messages.error(request, "User does not exist.")

        # If the login fails, render the login page again with error messages
        return render(request, 'store/login.html')


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class CartView(viewsets.ViewSet):
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
        serializer = CartSerializer(cart, many=True)

        return Response(serializer.data)
