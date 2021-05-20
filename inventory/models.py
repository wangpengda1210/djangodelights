from django.db import models


# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=200)
    price_per_unit = models.FloatField(default=0)

    def get_absolute_url(self):
        return '/ingredients'


class MenuItem(models.Model):
    title = models.CharField(max_length=200, unique=True, null=False)
    price = models.FloatField(default=0)

    def get_absolute_url(self):
        return '/menu_items'

    def available(self):
        return all(i.enough() for i in self.reciperequirement_set.all())


class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)

    def get_absolute_url(self):
        return '/menu_items'

    def enough(self):
        return self.quantity <= self.ingredient.quantity


class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return '/purchases'
