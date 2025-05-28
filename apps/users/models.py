from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone

# Create your models here.
class Role(models.Model):
    class Meta:
        db_table = 'tbl_roles'
    
    role_id = models.BigAutoField(primary_key=True, blank=False)
    role_type = models.CharField(max_length=20, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class CustomUserManager(UserManager):
    def _create_user(self, username, email, full_name, password, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("You have not provided a valid email address")
        if not full_name:
            raise ValueError("Full name is required")
        if not password:
            raise ValueError("Password is required!")
        
        email = self.normalize_email(email)
        
        user = self.model(
            username=username,
            email=email,
            full_name=full_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username=None, email=None, full_name=None, password=None, role=None, profile=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, full_name, password, role, profile, **extra_fields)

    def create_superuser(self, username, email, full_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, full_name, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, blank=True, default='', unique=True)
    email = models.EmailField(blank=False, default='', unique=True)
    full_name = models.CharField(max_length=255, blank=False, default='')
    password = models.CharField(max_length=255, blank=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, default='1', blank=False)
    profile = models.ImageField(null=True, default='', blank=True, upload_to='profiles/')
    
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'full_name', 'password']

    class Meta:
        db_table = 'tbl_users'

    def get_full_name(self):
        return self.name