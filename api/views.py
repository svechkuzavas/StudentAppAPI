from rest_framework import viewsets, status
from rest_framework.authtoken.serializers import *
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import *


class HelloView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        """
        :param request:
        :return:
        """
        content = {'message': 'Hello, World!'}
        return Response(content)


class UserCreateView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post', 'get']


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    http_method_names = ['get', 'put']
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['GET'])
    def get_full_data(self, request, pk=None):
        user_profile = self.get_object()
        user = User.objects.get(pk=user_profile.user.pk)
        return Response({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'group': user_profile.group,
            'role': user_profile.role,
            'image_url': user_profile.image.url[8:],
        })

    @action(detail=True, methods=['PUT'])
    def set_group(self, request, pk=None):
        user_profile = self.get_object()
        serializer = UserProfileSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            user_profile.group = serializer.validated_data['group']
            user_profile.save()
            return Response({'success': True, 'changes': {'group': user_profile.group}})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticated,)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticated,)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        context = {
            'token': token.key,
            'user_id': token.user_id,
            'profile_id': '0',
        }
        user_profile = UserProfile.objects.get(user__id=token.user_id)
        if user_profile:
            context['profile_id'] = user_profile.pk

        return Response(context)