from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название катергории')

    def __str__(self):
        return self.name


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Код категории')
    name = models.CharField(max_length=50, verbose_name='Название товара')
    price = models.FloatField(verbose_name='Цена товара')

    def __str__(self):
        return self.name


class Order(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Код товара')
    quantity = models.IntegerField(verbose_name='Количество товара')
