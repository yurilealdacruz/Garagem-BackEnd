# ProjectVehicle/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


# Serializers definem a representação da API.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets definem o comportamento da visualização.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers fornecem uma maneira fácil de determinar automaticamente o conf de URL.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('polls.urls')),  # Certifique-se de que isso está correto
    path('', include(router.urls)),  # Inclua as rotas do roteador aqui
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] 

