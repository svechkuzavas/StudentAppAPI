from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status
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
    http_method_names = ['post']
    permission_classes = (IsAuthenticated,)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    http_method_names = ['get', 'put']
    permission_classes = (IsAuthenticated,)

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


