from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated

# View to update the profile
class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

# View to get a profile by nickname
class ProfileDetailView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    lookup_field = 'username'
    queryset = Profile.objects.all()

# View to get all profiles
class ProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


from rest_framework.views import APIView
from rest_framework.response import Response

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Только аутентифицированные пользователи

    def get(self, request, *args, **kwargs):
        # Получаем профиль текущего пользователя через request.user

        print(request.user)
        profile = Profile.objects.get(user=request.user)  # предполагается, что у пользователя есть связанный профиль
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)