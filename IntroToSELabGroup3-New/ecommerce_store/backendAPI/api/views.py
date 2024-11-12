from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.response import Response
from api.serializers import CartSerializer, OrderSerializer
from api.models import User, StoreStock, Cart, Order, OrderDetails, ShippingInformation, CartItem
from django.contrib.auth.decorators import login_required

# View Functions for Rendering Templates
def gethome(request):
    return render(request, "store/home.html")


def getcontact(request):
    return render(request, "store/contact.html")


def getbase(request):
    return render(request, "store/base.html")


def getabout(request):
    return render(request, "store/about.html")


def getadmin(request):
    return render(request, "store/admin.html")


def getproduct(request):
    return render(request, "store/products.html")

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
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

def getregister(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        account_type = request.POST.get('account_type')

        # Check if account type is selected
        if not account_type:
            return render(request, 'store/register.html', {
                'error_message': "Please select an account type."
            })

        # Validate passwords match
        if password1 != password2:
            return render(request, 'store/register.html', {
                'error_message': "Passwords don't match. Please try again."
            })

        try:
            # Use create_user to ensure the password is hashed
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                account_type=account_type
            )
            user.save()

            # Log in the user after registration
            login(request, user)
            return redirect('home')
        except Exception as e:
            return render(request, 'store/register.html', {
                'error_message': f"An error occurred: {str(e)}. Please try again."
            })
    else:
        return render(request, 'store/register.html')




# Cart Management Views
@login_required
def update_cart(request, product_id):
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            messages.error(request, "Your cart could not be found.")
            return redirect('cart')

        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity)
            if quantity <= 0:
                CartItem.objects.filter(cart=cart, product_id=product_id).delete()
                messages.success(request, "Item removed from the cart.")
            else:
                product = get_object_or_404(StoreStock, id=product_id)
                if quantity > product.stock_quantity:
                    messages.error(request, "Requested quantity exceeds available stock.")
                    return redirect('cart')

                cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, "Cart updated successfully.")
        except ValueError:
            messages.error(request, "Invalid quantity.")
            return redirect('cart')

        return redirect('cart')


@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if cart_item:
            cart_item.delete()
        else:
            print("Cart item not found.")
    return redirect('cart')


@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Get the product and quantity from the request data
        try:
            product = StoreStock.objects.get(id=product_id)
        except StoreStock.DoesNotExist:
            return JsonResponse({"error": "Product not found."}, status=404)

        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity)
            if quantity <= 0:
                return JsonResponse({"error": "Quantity must be greater than zero."}, status=400)

            if quantity > product.stock_quantity:
                return JsonResponse({"error": "Requested quantity exceeds available stock."}, status=400)

            # Get or create the cart item and update the quantity
            cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not item_created:
                cart_item.quantity += quantity
                if cart_item.quantity > product.stock_quantity:
                    return JsonResponse({"error": "Total requested quantity exceeds available stock."}, status=400)
            else:
                cart_item.quantity = quantity

            cart_item.save()
            cart.save()

        except ValueError:
            return JsonResponse({"error": "Invalid quantity."}, status=400)

        return JsonResponse({"message": "Item added to cart successfully."}, status=201)

    return HttpResponseBadRequest("Invalid request method.")


# Class-Based Views
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


class RegisterView(View):
    def get(self, request):
        # Display registration form
        return render(request, 'store/register.html')

    def post(self, request):
        # Handle form submission
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        account_type = request.POST.get('account_type')

        # Check if account type is selected
        if not account_type:
            return render(request, 'store/register.html', {
                'error_message': "Please select an account type."
            })

        # Validate passwords match
        if password1 != password2:
            return render(request, 'store/register.html', {
                'error_message': "Passwords don't match. Please try again."
            })

        # Check if the username already exists
        if get_user_model().objects.filter(username=username).exists():
            return render(request, 'store/register.html', {
                'error_message': "Username already exists. Please choose another one."
            })

        try:
            # Use create_user to hash the password and save the user properly
            user = get_user_model().objects.create_user(
                username=username,
                email=email,
                password=password1,  # `create_user` will automatically hash this password
                account_type=account_type
            )
            user.save()

            # Log in the user after successful registration
            login(request, user)
            return redirect('home')
        except Exception as e:
            # Handle other exceptions (e.g., duplicate email or database errors)
            return render(request, 'store/register.html', {
                'error_message': f"An error occurred: {str(e)}. Please try again."
            })

class LoginView(View):
    def get(self, request):
        return render(request, 'store/login.html')

    def post(self, request):
        # Retrieve username and password from POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Debugging: Print entered credentials
        print(f"[DEBUG] Entered Username: {username}")
        print(f"[DEBUG] Entered Password: {password}")

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user:
            print("[DEBUG] Authentication successful.")
            login(request, user)
            return redirect('cart_html')
        else:
            try:
                db_user = User.objects.get(username=username)
                print(f"[DEBUG] Stored Hashed Password: {db_user.password}")
            except User.DoesNotExist:
                print("[DEBUG] User does not exist in the database.")

            print("[DEBUG] Authentication failed. Password mismatch or user not found.")
            messages.error(request, "Invalid username or password.")
            return render(request, 'store/login.html')

def logout_view(request):
    # Log the user out
    logout(request)

    return redirect('login')


# Viewsets for API Endpoints
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

        try:
            product = StoreStock.objects.get(id=product_id)
        except StoreStock.DoesNotExist:
            return Response({"error": "Product not found."}, status=404)

        if quantity > product.stock_quantity:
            return Response({"error": "Not enough stock available."}, status=400)

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

def products_view(request):
    products = StoreStock.objects.all()
    return render(request, 'store/products.html', {'products': products})

def product_detail_view(request, product_id):
    product = get_object_or_404(StoreStock, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})