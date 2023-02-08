from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status, filters
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers, models, permissions

# Create your views here.
class HelloApiView(APIView):

    """ ApiView de prueba"""

    serializer_class = serializers.HelloSerializer

    def get(self, request, forma=None):
        """Retornar lista de carateristicas"""

        an_apiview = [
            "Usamos metodos HTTP como funciones (get, post, path, put, delete)",
            "Es una vista similar a una vista tradicional de django",
            "nos da mayor control sobre la logica de nuestra aplicacion",
            "Esta mapeado manuamente los URLs",
        ]
        pruebalist = {
            "nuevo": "dos",
            "nuevo1": "tres",
        }
        return Response({"mesage": pruebalist, "an_apiview":an_apiview, "texto": "Hola mundo"})

    def post(self, request):
        """ Crea un mensaje con nuestro nombre """

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f'Hello {name}'

            return Response({"message": message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def put(self, request, pk=None):
        """ Maneja actualizar un objeto """

        return Response({"metod": "PUT"})

    def patch(self, request, pk=None):
        """ Maneja actualizacion parcial de un obejto"""

        return Response({"metod": "PATCH"})

    def delete(self, request, pk=None):
        """ Borrrar un objeto """

        return Response({"metod": "DELETE"})
    

class HelloViewSet(viewsets.ViewSet):
    """ Test apiviewset """

    serializer_class = serializers.HelloSerializer


    def list(self, request):
        """ Retornar mensajes de hola mundo """

        a_viewset = [
            "usa acciones (list, create, retieve, update, partial_update)", 
            "Automaticamente mapea a los URLs unsando Routers",
            "Provee mas funcionalidad con menos codigo"
        ]
        return Response({"message": "hola", "a_viewset": a_viewset})    

    def create(self, request):
        """ Crear nuevo mensaje de hola mundo"""

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f'hola {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """ Obtiene un objeto y su ID """

        return Response({"http_method": "GET"})
    
    def update(self, request, pk=None):
        """ Actualiza un objeto """

        return Response({"http_method": "PUT"})

    def partial_update(self, request, pk=None):
        """ Actualiza parcialmente el objeto """

        return Response({"http_method": "PATCH"})

    def destroy(self, request, pk=None):
        """ Destruye un objeto """

        return Response({"http_method": "DELETE"})

class UserProfileViewSet(viewsets.ModelViewSet):
    """ Crear y actualizar los perfiles """

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class UserLoginApiView(ObtainAuthToken):
    """  Crea tokens de autenticacion de usario """

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """ Maneja el crear, leer y actualizar el profile feed """
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnProfile, IsAuthenticated)

    def perform_create(self, serializer):
        """ Setear el perfil de usuario para el usuario que este logeado """
        serializer.save(user_profile = self.request.user)
        
