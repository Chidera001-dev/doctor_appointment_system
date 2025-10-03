from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import UserCreationSerializer, UserSerializer

User = get_user_model()


class UserCreateView(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_summary="Create a user account")
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # ✅ Return saved user data
        return Response(
            UserCreationSerializer(user).data,  # show created user info
            status=status.HTTP_201_CREATED,
        )


# Create your views here.
