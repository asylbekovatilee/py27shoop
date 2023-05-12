
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from .utils import send_activation_code



class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, phone, **kwargs):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **kwargs)
        # self.model = User
        user.set_password(password)  # хеширование пароля
        user.create_activation_code()  # генерируем ак.код
        send_activation_code(user.email, user.activation_code) 
        user.save(using=self._db)  # созраняем юзера в бд
        return user

    def create_superuser(self, email, password, phone, **kwargs):
        if not email:
            raise ValueError("Email is required")
        kwargs["is_staff"] = True  # даем права суперадмина
        kwargs["is_superuser"] = True
        kwargs["is_active"] = True
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **kwargs)
        # self.model = User
        user.set_password(password)  # хеширование пароля
        #отправляем на почту
        user.save(using=self._db)  # созраняем юзера в бд
        return user


class User(AbstractUser):
    username = None 
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    bio = models.TextField()

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['phone']

    objects = UserManager() 
