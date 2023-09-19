from django.db import models
from django.core.validators import MinValueValidator,RegexValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)  
from django.forms import ValidationError
import datetime
from django.db.models.query import QuerySet


class Game(models.Model):
    """MY GAME!"""

    name: str = models.CharField(
        verbose_name='игра',
        max_length=200
    )
    price: float = models.DecimalField(
        verbose_name='цена',
        max_digits=11,
        decimal_places=2,
        validators=[
            MinValueValidator(0, message='Мы деньги за игры не даём!')
        ]
    )
    poster: str = models.ImageField(
        verbose_name='постер',
        upload_to='posters'
    )
    rate: float = models.FloatField(
        verbose_name='рейтинг',
        max_length=5
    )

class MyUserManager(BaseUserManager):
    """ClientManager."""

    def create_user(
        self,
        email: str,
        password: str
    ) -> 'MyUser':
        if not email:
            raise ValidationError('Email required')

        custom_user: 'MyUser' = self.model(
            email=self.normalize_email(email),
            password=password
        )
        custom_user.set_password(password)
        custom_user.save(using=self._db)
        return custom_user

    def create_superuser(
        self,
        email: str,
        password: str
    ) -> 'MyUser':

        custom_user: 'MyUser' = self.model(
            email=self.normalize_email(email),
            password=password
        )
        custom_user.is_superuser = True
        custom_user.is_active = True
        custom_user.is_staff = True
        custom_user.set_password(password)
        custom_user.save(using=self._db)
        return


class MyUser(AbstractBaseUser, PermissionsMixin):
    class Currencies(models.TextChoices):
        TENGE = 'KZT', 'Tenge'
        RUBLI = 'RUB', 'Rubli'
        EURO = 'EUR', 'Euro'
        DOLLAR = 'USD', 'Dollar'


    email =  models.EmailField(
        verbose_name='почта/логин',
        max_length=200,
        unique=True
    )
    nickname = models.CharField(
        verbose_name='ник',
        max_length=120
    )
    currency = models.CharField(
        verbose_name='валюта',
        max_length=4,
        choices=Currencies.choices,
        default=Currencies.TENGE
    )
    is_staff = models.BooleanField(
        verbose_name='staff',
        default=False
    )

    objects = MyUserManager()
    
    @property
    def balance(self) -> float:
        transactions: QuerySet[Transaction] = \
            Transaction.objects.filter(user=self.pk)
        result: float = 0
        for trans in transactions:
            if trans.is_filled:
                result += trans.amout
            else:
                result -= trans.amout
        return result


    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = (
            '-id',
        )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Transaction(models.Model):
    user = models.ForeignKey(
        verbose_name='пользователь',
        related_name='transactions',
        to=MyUser,
        on_delete=models.PROTECT
    )
    amount = models.DecimalField(
        verbose_name='сумма',
        max_digits=11,
        decimal_places=2
    )
    datetime_created = models.DateField(
        verbose_name='дата транкзации',
        auto_now_add=True,
    )
    is_filled = models.BooleanField(
        verbose_name='пополнение?',
        default=False
    )

    class Meta:
        ordering = ('-datetime_created',)
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

class Comment(models.Model):

    """Comment for games and comp."""
    
    user = models.ForeignKey(
        verbose_name='кто оставил',
        to=MyUser,
        related_name='comments',
        on_delete=models.CASCADE
    )
    text = models.CharField(
        verbose_name='текст',
        max_length=254
    )
    rate = models.IntegerField(
        verbose_name='рейтинг',
    )
    datetime_created = models.DateTimeField(
        verbose_name='дата создания',
        null=True,
        blank=True
    )
    game = models.ForeignKey(
        verbose_name='игра',
        related_name='game_comments',
        to=Game,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self) -> str:

        rate_str = '★' * self.rate 
        return f'{self.user.username} оценка:   {rate_str}'


# Создать форму для создания игры и редактирования игры
# Реализовать создание и удаление игры
