from django.contrib.auth import get_user_model, login

from rest_framework import generics

from shop_api.models import (
    Product,
    Order
)
from shop_api.serializers import (
    ProductSerializer,
    OrderSerializer,
)

User = get_user_model()

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveDestroyAPIView

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    TokenSerializer
)


class UserRegistrationAPIView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegistrationSerializer


class UserLoginAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response(
                data={"token": token.key},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserTokenAPIView(RetrieveDestroyAPIView):
    lookup_field = "key"
    serializer_class = TokenSerializer
    queryset = Token.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def retrieve(self, request, key, *args, **kwargs):
        if key == "current":
            instance = Token.objects.get(key=request.auth.key)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return super(UserTokenAPIView, self).retrieve(request, key, *args, **kwargs)

    def destroy(self, request, key, *args, **kwargs):
        if key == "current":
            Token.objects.get(key=request.auth.key).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super(UserTokenAPIView, self).destroy(request, key, *args, **kwargs)


class ProductListAPIView(generics.ListAPIView):
    """
        API endpoint for listing products.
    """
    serializer_class = ProductSerializer
    permission_classes = ()

    def get_queryset(self):
        return Product.objects.all()


class OrderListAPIView(generics.ListAPIView):
    """
        API endpoint for listing orders.
    """
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.id)


class OrderCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
