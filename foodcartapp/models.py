import phonenumbers
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.utils.functional import cached_property


class Restaurant(models.Model):
    name = models.CharField('название', max_length=50)
    address = models.CharField('адрес', max_length=100, blank=True)
    contact_phone = models.CharField('контактный телефон', max_length=50, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'


class ProductQuerySet(models.QuerySet):
    def available(self):
        return self.distinct().filter(menu_items__availability=True)


class ProductCategory(models.Model):
    name = models.CharField('название', max_length=50)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('название', max_length=50)
    category = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name='категория', related_name='products')
    price = models.DecimalField('цена', max_digits=8, decimal_places=2)
    image = models.ImageField('картинка')
    special_status = models.BooleanField('спец.предложение', default=False, db_index=True)
    ingridients = models.CharField('ингредиенты', max_length=200, blank=True)

    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='menu_items')
    availability = models.BooleanField('в продаже', default=True, db_index=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]


class Order(models.Model):
    ORDER_STATUSES = (
        ('0', 'Получен'),
        ('1', 'Передан ресторану'),
        ('2', 'Передан курьеру'),
        ('3', 'Доставлен'),
    )
    PAYMENT_METHODS = (
        ('0', 'Наличные'),
        ('1', 'Картой онлайн'),
    )

    firstname = models.CharField('Имя', max_length=30)
    lastname = models.CharField('Фамилия', max_length=30)
    phonenumber = models.CharField('Номер телефона', max_length=20)
    phone_number_pure = PhoneNumberField('Нормализованный номер телефона', blank=True)
    address = models.CharField('Адресс', max_length=200)
    order_status = models.CharField('Статус заказа', max_length=1, choices=ORDER_STATUSES, default='0')
    comment = models.TextField('Комментарий', default='')

    registrated_at = models.DateTimeField('Получен в', default=timezone.now, blank=True, null=True)
    called_at = models.DateTimeField('Прозвонен в', blank=True, null=True)
    delivered_at = models.DateTimeField('Доставлен в', blank=True, null=True)

    payment_method = models.CharField('Метод оплаты', max_length=1, choices=PAYMENT_METHODS, default='0')

    @cached_property
    def cart_total(self):
        return self.order_products.all().aggregate(cart_total=Sum('product_total'))

    def save(self, *args, **kwargs):
        if not self.phone_number_pure:
            try:
                parsed_phone_number = phonenumbers.parse(self.phonenumber, "RU")
                self.phone_number_pure = phonenumbers.format_number(parsed_phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            except phonenumbers.NumberParseException:
                pass
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.pk}. {self.firstname} {self.lastname}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='order_products')
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, verbose_name='Продукт')
    quantity = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Количество')
    product_total = models.DecimalField('цена', null=True, max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.product_total:
            self.product_total = self.product.price * self.quantity
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.product.name
