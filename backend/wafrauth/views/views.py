from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.permissions import IsAuthenticated
from wafrauth.serializers import UserSerializer, CreateUserSerializer, UserDetailSerializer
from wafrauth.permissions import IsOwnerOrReadOnly

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    def get_authenticate_header(self, request):
        try:
            email = request.data.get('email', None)
            user = User.objects.filter(email=email).first()
        except Exception as ex:
            print(ex)
        return super().get_authenticate_header(request)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        email = request.data['email']
        user = User.objects.filter(email=email)
        if not user.exists():
            return Response("Invalid Email", status=status.HTTP_400_BAD_REQUEST)
        user = user.first()
        if not user.is_verified:
            return Response("You haven't verify your account.", status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = User.objects.all().order_by('id')
    serializer_classes = {
        'retrieve': UserDetailSerializer
    }
    default_serializer_class = UserSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)


    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = CreateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, **kwargs):
        user = self.get_object()
        if request.user.is_superuser:
            user.delete()
            message = 'Deleted successfully'
            return Response(message, status=status.HTTP_204_NO_CONTENT)
        message = 'Only superuser can delete an account'
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

