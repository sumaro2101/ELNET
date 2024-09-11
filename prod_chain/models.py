from django.db import models
from django.urls import reverse

from django_countries.fields import CountryField


class Product(models.Model):
    """Модель продукта
    """
    name = models.CharField(max_length=254,
                            verbose_name='название',
                            help_text='название продукта',
                            )

    model = models.CharField(max_length=254,
                             verbose_name='модель',
                             help_text='модель продукта',
                             )

    realize = models.DateField(verbose_name='дата выхода',
                               help_text='Дата выхода продукта на рынок',
                               )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})


class Contact(models.Model):
    """Модель контакта объекта
    """
    CHOICE_ROLE = {
        'factory': 'Завод',
        'retail': 'Розничная сеть',
        'entrepreneur': 'Предприниматель'
    }

    name = models.CharField(max_length=250,
                            verbose_name='имя',
                            help_text='Имя сети или завода')

    role = models.CharField(max_length=50,
                            choices=CHOICE_ROLE,
                            verbose_name='Тип роли',
                            help_text='Какую роль исполняет объект',
                            )

    email = models.EmailField(max_length=254,
                              verbose_name='Email',
                              help_text='Email контакта',
                              )

    country = CountryField(verbose_name='страна',
                           db_index=True,
                           help_text='Страна контакта',
                           )

    town = models.CharField(max_length=254,
                            verbose_name='город',
                            db_index=True,
                            help_text='Город контакта',
                            )

    street = models.CharField(max_length=254,
                              verbose_name='улица',
                              help_text='Улица контакта',
                              )

    build = models.CharField(max_length=10,
                             verbose_name='дом',
                             help_text='Номер дома контакта',
                             )

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'
        constraints = [models.UniqueConstraint(
            fields=['name',
                    'role',
                    'country',
                    ],
            name='unique_contact',
            ),]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("contact_detail", kwargs={"pk": self.pk})


class ProdMap(models.Model):
    """Модель сети
    """
    prod_object = models.ForeignKey("prod_chain.Contact",
                                    verbose_name='объект',
                                    on_delete=models.PROTECT,
                                    help_text='Целевой объект цепочки',
                                    )

    products = models.ManyToManyField("prod_chain.Product",
                                      verbose_name='товары',
                                      help_text='Товары объекта',
                                      )

    supplier = models.ForeignKey("self",
                                 verbose_name='поставщик',
                                 on_delete=models.PROTECT,
                                 help_text='Поставщик',
                                 null=True,
                                 blank=True,
                                 )

    duty = models.DecimalField(max_digits=13,
                               decimal_places=2,
                               verbose_name='долг',
                               help_text='Долг перед поставщиком',
                               )

    appoiment_date = models.DateTimeField(auto_now_add=True,
                                          verbose_name='дата',
                                          help_text='Дата назначения',
                                          )

    class Meta:
        verbose_name = "сеть"
        verbose_name_plural = "сети"

    def __str__(self):
        return str(self.appoiment_date)

    def get_absolute_url(self):
        return reverse("map_detail", kwargs={"pk": self.pk})
