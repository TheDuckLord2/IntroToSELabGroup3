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
    return render(request, "store\\cart.html")

def getlogin(request):
    return render(request, "store\\login.html")

def getproduct(request):
    return render(request, "store\\product.html")


#returns static data, used to make sure a webpage can work
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

#returns dynamic data from a table in the database
#viewsets.ModelViewSet handles CRUD which is needed for database output
class UserCreationView(viewsets.ModelViewSet):
    #queryset grabs all entries from table
    queryset = UserCreation.objects.all()
    #serializes all the data gathered into a presentable JSON format
    serializer_class = UserCreationSerializer
    #lists all data in JSON format
    def list(self, request):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        #Response formats an HTTP response for the data
        return Response(serializer.data)


class RegisterView(viewsets.ModelViewSet):
    queryset = CreatedUser.objects.all()
    serializer_class = CreatedUserSerializer

    def login(self, request):
        username = request.query_params.get('username', None)
        password = request.query_params.get('password', None)

        if not username:
            return Response({"Invalid Entry: Please enter an email."},status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({"Invalid Entry: Please enter a password."},status=status.HTTP_400_BAD_REQUEST)

        try:
            user_username = CreatedUser.objects.get(username=username)
            user_password = CreatedUser.objects.get(password=password)
            return Response({"Login Successful."},status=status.HTTP_200_OK)

        except CreatedUser.DoesNotExist:
            return Response({"Username or Password does not exist."},status=status.HTTP_400_BAD_REQUEST)


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
