from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    "Класс-генерик для создания пользователя"
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
