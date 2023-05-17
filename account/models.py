from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from .tasks import send_activation_code


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
        send_activation_code.delay(user.email, user.activation_code) 
        Billing.objects.create(user=user)
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
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=8, blank=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['phone']

    objects = UserManager() 


    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        code = get_random_string(length=8)
        self.activation_code = code
        self.save()

class Billing(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='billing')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def top_up(self, amount):
        """пополнение счета если транзакция прошла успешно вернется True"""
        if amount > 0:
            self.amount += amount
            self.save()
            return True
        return False
    
    def withdraw(self, amount):
        """снятие денег со счета если  транзакция прошла успешно вернется True"""
        if self.amount >= amount:
            self.amount -= amount
            self.save()
            return True
        return False
    
    
    

