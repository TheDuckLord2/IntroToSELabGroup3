

from django.http import JsonResponse,  HttpResponseBadRequest
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.response import Response
from api.serializers import CartSerializer, OrderSerializer
from api.models import User, StoreStock, Cart, Order, OrderDetails,  CartItem
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.urls import reverse
from django.db import transaction




def gethome(request):
    cart_items = None
    if request.user.is_authenticated:
        # Get the cart for the authenticated user
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_items = CartItem.objects.filter(cart=cart)

    context = {
        'cart': cart_items  # Pass the cart items to the template
    }
    return render(request, "store/home.html", context)


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

def product_search(request):
    query = request.GET.get('q', '')
    products = StoreStock.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query))

    return render(request, 'products/search_results.html', {'products': products, 'query': query})

@login_required(login_url='login')
def getcart(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        context = {
            'cart_items': None,
            'total': 0,
        }
        return render(request, 'store/cart.html', context)

    cart_items = CartItem.objects.filter(cart=cart)

    total = sum(item.product.price * item.quantity for item in cart_items)

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

        if not account_type:
            return render(request, 'store/register.html', {
                'error_message': "Please select an account type."
            })

        if password1 != password2:
            return render(request, 'store/register.html', {
                'error_message': "Passwords don't match. Please try again."
            })

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                account_type=account_type
            )
            user.save()

            login(request, user)
            return redirect('home')
        except Exception as e:
            return render(request, 'store/register.html', {
                'error_message': f"An error occurred: {str(e)}. Please try again."
            })
    else:
        return render(request, 'store/register.html')

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



class StaticDataView(View):
    def get(self, request):
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
        return render(request, 'store/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        account_type = request.POST.get('account_type')

        if not account_type:
            return render(request, 'store/register.html', {
                'error_message': "Please select an account type."
            })

        if password1 != password2:
            return render(request, 'store/register.html', {
                'error_message': "Passwords don't match. Please try again."
            })

        if get_user_model().objects.filter(username=username).exists():
            return render(request, 'store/register.html', {
                'error_message': "Username already exists. Please choose another one."
            })

        is_staff = True if account_type == 'Seller' else False

        try:
            user = get_user_model().objects.create_user(
                username=username,
                email=email,
                password=password1,
                account_type=account_type,
                is_staff=is_staff
            )
            user.save()

            messages.success(request, "Account created successfully! Please log in on home page.")

            return render(request, 'store/register.html')

        except Exception as e:
            return render(request, 'store/register.html', {
                'error_message': f"An error occurred: {str(e)}. Please try again."
            })

class LoginView(View):
    def get(self, request):
        account_type = request.GET.get('account_type')
        readable_account_types = {
            'buyer': 'Buyer',
            'seller': 'Seller',
            'admin': 'Admin',
        }
        human_readable_type = readable_account_types.get(account_type)

        return render(request, 'store/login.html', {
            'account_type': account_type,
            'human_readable_type': human_readable_type
        })

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        account_type = request.POST.get('account_type')

        print(f"[DEBUG] Entered Username: {username}")
        print(f"[DEBUG] Entered Password: {password}")
        print(f"[DEBUG] Expected Account Type: {account_type}")

        user = authenticate(request, username=username, password=password)

        if user:
            if account_type and user.account_type.lower() != account_type:
                print(f"[DEBUG] Account type mismatch. Expected {account_type}, got {user.account_type}")
                messages.error(request, f"Login only for {account_type}s only.")
                return redirect(f"{reverse('login')}?account_type={account_type}")

            print("[DEBUG] Authentication successful.")
            login(request, user)
            return redirect('home')
        else:
            try:
                db_user = User.objects.get(username=username)
                print(f"[DEBUG] Stored Hashed Password: {db_user.password}")
            except User.DoesNotExist:
                print("[DEBUG] User does not exist in the database.")

            print("[DEBUG] Authentication failed. Password mismatch or user not found.")
            messages.error(request, "Invalid username or password.")
            return redirect(f"{reverse('login')}?account_type={account_type}")


def logout_view(request):
    logout(request)

    return redirect('home')


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
    query = request.GET.get('q', '')
    products = StoreStock.objects.filter(is_approved=True)

    if query:
        products = products.filter(Q(name__icontains=query))

    return render(request, 'store/products.html', {'products': products, 'query': query})

def product_detail_view(request, product_id):
    product = get_object_or_404(StoreStock, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


def getmanage(request):
    storestock = StoreStock.objects.all()  # Adjust based on your data
    return render(request, 'store/manage.html', {'storestock': storestock})

def new_product(request):
    if request.method == 'POST':
        name = request.POST.get('productname')
        quantity = request.POST.get('productquantity')
        price = request.POST.get('productprice')
        description = request.POST.get('productdesc')
        image = request.FILES.get('productimage')
        seller_id = request.user.id

        StoreStock.objects.create(
            name=name,
            stock_quantity=quantity,
            price=price,
            description=description,
            image=image,
            seller_id=seller_id,
        )

        messages.success(request, "New product added successfully!")
        return redirect('manage')

    return render(request, 'store/manage.html')


def update_storestock(request, item_id):
    item = get_object_or_404(StoreStock, id=item_id)

    if request.method == 'POST':
        item.name = request.POST.get('productname', item.name)
        item.stock_quantity = request.POST.get('productquantity', item.stock_quantity)
        item.price = request.POST.get('productprice', item.price)
        item.description = request.POST.get('productdesc', item.description)

        if 'productimage' in request.FILES:
            item.image = request.FILES['productimage']

        item.save()
        return redirect('manage')

    return render(request, 'store/update_storestock.html', {'item': item})

def remove_from_storestock(request, item_id):
    item = get_object_or_404(StoreStock, id=item_id)
    item.delete()
    return redirect('manage')

@login_required
def manage_products_view(request):
    if request.user.account_type == 'Seller':
        storestock = StoreStock.objects.filter(seller=request.user)
    else:
        storestock = []

    return render(request, 'store/manage.html', {'storestock': storestock})

def approve_product(request, item_id):
    if request.method == "POST":
        product = get_object_or_404(StoreStock, id=item_id)
        product.is_approved = True
        product.save()
    return redirect('admin')


def reject_product(request, item_id):
    if request.method == "POST":
        product = get_object_or_404(StoreStock, id=item_id)
        product.delete()
    return redirect('admin')


def admin_dashboard(request):
    storestock = StoreStock.objects.all()
    user_table = User.objects.filter(is_superuser=True)
    return render(request, 'store/admin.html', {'storestock': storestock, 'user_table': user_table})



@login_required
def process_payment(request):
    if request.method == "POST":
        payment_successful = True

        if payment_successful:
            try:
                with transaction.atomic():
                    cart = Cart.objects.filter(user=request.user).first()
                    if not cart:
                        raise ValueError("Cart not found!")

                    total_price = sum(item.product.price * item.quantity for item in cart.items.all())

                    # Create the order
                    order = Order.objects.create(
                        user=request.user,
                        total_price=total_price,
                        status='pending'
                    )

                    # Create order details and update product stock
                    for cart_item in cart.items.all():
                        OrderDetails.objects.create(
                            order=order,
                            item=cart_item.product,
                            quantity=cart_item.quantity,
                            price=cart_item.product.price
                        )

                        # Update stock quantity
                        cart_item.product.stock_quantity -= cart_item.quantity
                        if cart_item.product.stock_quantity < 0:
                            raise ValueError(f"Not enough stock for {cart_item.product.name}")
                        cart_item.product.save()

                    # Clear the cart
                    cart.items.all().delete()

                    # Show success message
                    messages.success(request, "Payment processed successfully! Your order has been placed.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}. Please try again.")

            return redirect('cart_html')

    return redirect('cart_html')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(StoreStock, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()

    # Redirect to the cart page
    return redirect('cart_html')

@login_required
def user_profile(request):
    orders = Order.objects.filter(user=request.user)
    cart = Cart.objects.filter(user=request.user).first()
    has_management_permission = request.user.has_perm('app.view_management')
    is_manager = request.user.groups.filter(name='manager').exists()

    cart_items = cart.items.count() if cart else 0

    return render(
        request,
        'store/user.html',
        {
            'orders': orders,
            'cart': cart,
            'has_management_permission': has_management_permission,
            'is_manager': is_manager,
            'cart_items': cart_items,
        }
    )

@login_required
def update_profile(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')

        if new_username and new_email:
            request.user.username = new_username
            request.user.email = new_email
            request.user.save()
            messages.success(request, "Profile updated successfully!")
        else:
            messages.error(request, "Please provide both username and email.")

        return redirect('user_profile')

    # Render a form for updating the profile
    return render(request, 'store/update_profile.html', {'user': request.user})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_details = OrderDetails.objects.filter(order=order).annotate(total=F('quantity') * F('price'))

    return render(request, 'store/order_detail.html', {
        'order': order,
        'order_details': order_details,
    })
