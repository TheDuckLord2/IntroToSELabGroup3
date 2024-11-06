from django.shortcuts import render
from rest_framework.views import APIView
from django.views import View
from django.http import JsonResponse
from api.serializers import UserCreationSerializer
from api.serializers import CartSerializer
from api.serializers import CreatedUserSerializer
from api.models import UserCreation
from api.models import CreatedUser
from api.models import Cart
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



class CartView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    def list(self, request):
        cart = self.get_queryset()
        serializer = self.get_serializer(cart, many=True)

        return Response(serializer.data)