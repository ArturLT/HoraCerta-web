from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, nome, senha=None, nome_empresa=None):
        if not email:
            raise ValueError('O e-mail é obrigatório.')
        user = self.model(
            email=self.normalize_email(email),
            nome=nome,
            nome_empresa=nome_empresa
        )
        user.set_password(senha)
        user.save(using=self._db)
        return user

    # A função `create_superuser` foi corrigida para receber 'password'
    def create_superuser(self, email, nome, password=None):
        user = self.create_user(
            email,
            nome=nome,
            senha=password, # Passe o 'password' para a função 'create_user'
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    # ... (o resto do seu modelo User) ...
    nome = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    nome_empresa = models.CharField(max_length=150, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    def __str__(self):
        return self.nome
        
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser