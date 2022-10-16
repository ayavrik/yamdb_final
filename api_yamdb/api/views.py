from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import (viewsets,
                            permissions,
                            pagination,
                            filters,
                            mixins,
                            status)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from django_filters.rest_framework import DjangoFilterBackend

from .filters import TitleFilter
from .permissions import (IsAuthorOrReadOnly,
                          IsAdminUserOrReadOnly,
                          IsModeratorOrReadOnly,
                          IsUserOrReadOnly,
                          IsAdminUser)
from . import serializers
from reviews.models import Review, Title, Category, Genre


class MixinSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoryViewSet(MixinSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(MixinSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
        & (IsAdminUserOrReadOnly | IsModeratorOrReadOnly | IsAuthorOrReadOnly)
    ]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
        & (IsAdminUserOrReadOnly | IsModeratorOrReadOnly | IsAuthorOrReadOnly)
    ]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title__id=title_id)
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title__id=title_id)
        serializer.save(review=review, author=self.request.user)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = serializers.TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.TitleSerializerGet
        return serializers.TitleSerializer


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser, )
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    lookup_field = 'username'


class CurrentUserView(APIView):
    permission_classes = (IsUserOrReadOnly, )

    def get_object(self, pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request):
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        obj = self.get_object(pk=request.user.id)
        serializer = serializers.UserSerializer(
            obj,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            if 'role' not in serializer.validated_data:
                serializer.save()
                return Response(serializer.data)
            if request.user.role != 'user':
                serializer.save()
                return Response(serializer.data)
            serializer.validated_data.pop('role')
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class GetConfirmationCodeView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = serializers.ConfirmationCodeSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['username'] == 'me':
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            user = get_object_or_404(
                User,
                username=serializer.data.get('username')
            )
            token = default_token_generator.make_token(user)
            send_mail(
                'Токен авторизации',
                f'Вот твой токен {token}',
                'from@example.com',
                [serializer.data.get('email')],
                fail_silently=False
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetJwtTokenView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = serializers.JwtTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User,
                username=request.data.get('username')
            )
            confirmation_code = request.data.get('confirmation_code')
            if default_token_generator.check_token(user, confirmation_code):
                refresh = RefreshToken.for_user(user)
                context = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(context)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
