from datetime import datetime

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsSuperUser
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = (IsSuperUser,)
    lookup_field = "username"

    @action(
        methods=["get", "patch"],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request, pk=None):
        if request.method == "GET":
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data)
        if request.method == "PATCH":
            user = get_object_or_404(User, username=self.request.user)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.data, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(["POST"])
@permission_classes([AllowAny])
def send_confirmation_code(request):
    email = request.data["email"]
    username = email.split("@")[0]
    user = User.objects.create(
        username=username,
        email=email,
        last_login=datetime.now(),
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        "Confirmation code",
        f"{confirmation_code}",
        f"{settings.ADMIN_EMAIL}",  # Это поле "От кого"
        [f"{email}"],  # Это поле "Кому" (можно указать список адресов)
        fail_silently=False,  # Сообщать об ошибках («молчать ли об ошибках?»)
    )
    return Response(confirmation_code, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def send_token(request):
    email = request.data["email"]
    user = get_object_or_404(User, username=email.split("@")[0])
    confirmation_code = request.data["confirmation_code"]
    refresh = RefreshToken.for_user(user)
    response = {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
    }
    if default_token_generator.check_token(user, confirmation_code):
        user.is_active = True
        user.save()
        return JsonResponse(response)
    else:
        message = "Ops! Bad wrong!"
        return JsonResponse(
            {"status": "false", "message": message}, status=500
        )
