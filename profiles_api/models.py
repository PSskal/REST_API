from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings



class UserProfileManager(BaseUserManager):
    """ Manager para perfiles de Usuario """
    
    def create_user(self, email, name, password=None):
        """ Crear nuevo User profile"""
        if not email:
            raise ValueError('El usuario debe tener un email')

        email = self.normalize_email(email) #convertir en minusculas
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """modelo base de datos para usuario en el sistema"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]  

    def get_full_name(self):
        """obtener nombre completo del usuario"""
        return self.name

    def get_short_name(self):
        """obtener nombre corto del usuario"""
        return self.name

    def __str__(self):
        """ Retornar Cadena Representado a nuesto usuario"""
        return self.email
        
class ProfileFeedItem(models.Model):
    """ Perfil de Status Update """
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status_text = models.CharField(max_length=255)
    create_on = models.TimeField(auto_now_add=False)

    def __str__(self):
        return self.status_text
    
    