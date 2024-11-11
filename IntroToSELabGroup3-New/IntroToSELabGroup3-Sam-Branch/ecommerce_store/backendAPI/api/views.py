from django.shortcuts import render
from rest_framework.views import APIView
from django.views import View
from django.http import JsonResponse, HttpResponse
from api.serializers import UserSerializer
from api.serializers import CartSerializer
from api.serializers import OrderSerializer
from api.serializers import OrderDetailsSerializer
from api.serializers import ShippingDetailsSerializer
from api.models import User, StoreStock, Cart, Order, OrderDetails, ShippingInformation
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, get_user_model
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


from django.shortcuts import render
from api.models import Cart, CartItem

def getcart(request):
    # Retrieve the cart for the logged-in user
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        # If the cart doesn't exist, create an empty cart context
        context = {
            'cart_items': None,
            'total': 0,
        }
        return render(request, 'store/cart.html', context)

    # Get all items in the cart
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate the total price of the cart
    total = sum(item.product.price * item.quantity for item in cart_items)

    # Pass the cart items and total to the template
    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'store/cart.html', context)



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
        if request.method == "POST":
            # Get form data from POST request
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

        # Validate passwords match
        if password1 != password2:
            return render(request, 'store/signup.html', {
                'error_message': "Passwords don't match. Please try again."
            })
        
        try:
            # Create the user if not exists
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            # Auto-login the user after successful registration
            login(request, user)
            return redirect('home')  # Redirect to the home page after registration
        except Exception as e:
            return render(request, 'store/signup.html', {
                'error_message': f"An error occurred: {str(e)}. Please try again."
            })
        else:
            # Handle GET request (just show the empty form)
            return render(request, 'store/signup.html')


def getproduct(request):
    return render(request, "store\\products.html")

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from api.models import Cart, CartItem, StoreStock

@login_required
def update_cart(request, product_id):
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return redirect('cart')  # Redirect if the cart doesn't exist

        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity)
            if quantity <= 0:
                # Remove the item if the quantity is zero or less
                CartItem.objects.filter(cart=cart, product_id=product_id).delete()
            else:
                # Update the quantity of the item
                cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
                cart_item.quantity = quantity
                cart_item.save()
        except (ValueError, CartItem.DoesNotExist):
            # Handle errors like invalid quantity or cart item not found
            pass

        return redirect('cart')  # Redirect back to the cart page

@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        # Remove the item from the cart
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
    return redirect('cart')



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
                return redirect('cart_html')
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


from api.models import User, StoreStock, Cart, CartItem, Order, OrderDetails, ShippingInformation
from rest_framework import viewsets
from rest_framework.response import Response

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
        cart = self.get_queryset().first()
        if not cart:
            return Response({"error": "Cart not found."}, status=404)

        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        if not product_id:
            return Response({"error": "Product ID is required."}, status=400)
        if not quantity:
            return Response({"error": "Quantity is required."}, status=400)

        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response({"error": "Quantity must be greater than zero."}, status=400)
        except ValueError:
            return Response({"error": "Invalid quantity. Must be a positive integer."}, status=400)

        # Fetch the product
        try:
            product = StoreStock.objects.get(id=product_id)
        except StoreStock.DoesNotExist:
            return Response({"error": "Product not found."}, status=404)

        # Validate stock availability
        if quantity > product.stock_quantity:
            return Response({"error": "Not enough stock available."}, status=400)

        # Create or update the cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()
        cart.save()

        return Response(CartSerializer(cart).data, status=200)

    def remove_from_cart(self, request, pk=None):
        cart = self.get_queryset().first()
        if not cart:
            return Response({"error": "Cart not found."}, status=404)

        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"error": "Product ID is required."}, status=400)

        try:
            product = StoreStock.objects.get(id=product_id)
        except StoreStock.DoesNotExist:
            return Response({"error": "Product not found."}, status=404)

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()
            return Response({"message": "Product removed from cart."}, status=204)
        except CartItem.DoesNotExist:
            return Response({"error": "Product not in cart."}, status=404)

    def list(self, request):
        cart = self.get_queryset()
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data, status=200)
