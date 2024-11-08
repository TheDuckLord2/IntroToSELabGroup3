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
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.hashers import make_password

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
    return render(request, "store\\login.html")

def getregister(request):
    return render(request, "store\\register.html")

def getproduct(request):
    return render(request, "store\\products.html")


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
class UserCreationView(CreateView):
    model = UserCreation
    template_name = 'register.html'  # Your registration template
    fields = ['username', 'email', 'account_type']  # Specify fields you want to display in the form
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Hash the password before saving the user
        form.instance.password = make_password(self.request.POST.get('password'))
        return super().form_valid(form)


class LoginView(viewsets.ModelViewSet):
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