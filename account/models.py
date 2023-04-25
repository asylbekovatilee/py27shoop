from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, phone, **kwargs):
        if not email:
            raise ValueError("Email is required")
        kwargs["is_stuff"] = True
        kwargs["is_superuser"] = True
        kwargs["is_active"] = True
        email = self.normalize_email(email) # порядок почты normalize email
        user = self.model(email=email, phone=phone, **kwargs)
        #self.model = User
        user.set_password(password) # хеширование пароля
        user.save(using=self._db) # сохряняем юзера в бд
        return user

    def create_superuser(self, email, password, phone, **kwargs):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email) # порядок почты normalize email
        user = self.model(email=email, phone=phone, **kwargs)
        #self.model = User
        user.set_password(password) # хеширование пароля
        user.save(using=self._db) # сохряняем юзера в бд
        return user


class User(AbstractUser):
    username = None # убираем юзернейм из полей
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    bio = models.TextField()

    USERNAME_FIELD = 'email' # указываем какое поле использовать при логине
    REQUIRED_FIELDS = ['phone']
    objects = UserManager() # указываем нового юзера
