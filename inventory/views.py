from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout

from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from .forms import IngredientForm, MenuItemForm, RecipeRequirementForm


# Create your views here.
class IngredientsView(ListView):
    template_name = "inventory/ingredients_list.html"
    model = Ingredient


class IngredientCreateView(LoginRequiredMixin, CreateView):
    template_name = "inventory/ingredient_create.html"
    model = Ingredient
    form_class = IngredientForm


class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "inventory/ingredient_update.html"
    model = Ingredient
    form_class = IngredientForm


class MenuItemsView(ListView):
    template_name = "inventory/menu_items_list.html"
    model = MenuItem


class MenuItemCreateView(LoginRequiredMixin, CreateView):
    template_name = "inventory/menu_item_create.html"
    model = MenuItem
    form_class = MenuItemForm


class PurchasesView(ListView):
    template_name = "inventory/purchases_list.html"
    model = Purchase


class PurchaseCreateView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/purchase_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = [item for item in MenuItem.objects.all() if item.available()]
        return context

    def post(self, request, *args, **kwargs):
        menu_item_id = request.POST['menu_item']
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        requirements = menu_item.reciperequirement_set

        for requirement in requirements.all():
            required_ingredient = requirement.ingredient
            required_ingredient.quantity -= requirement.quantity
            required_ingredient.save()

        purchase = Purchase(menu_item=menu_item)
        purchase.save()

        return redirect('/purchases')


class RecipeRequirementCreateView(LoginRequiredMixin, CreateView):
    template_name = "inventory/recipe_requirement_create.html"
    model = RecipeRequirement
    form_class = RecipeRequirementForm


class ProfitView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/profit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_cost = 0.0
        revenue = 0.0

        for purchase in Purchase.objects.all():
            revenue += purchase.menu_item.price
            for requirement in purchase.menu_item.reciperequirement_set.all():
                total_cost += requirement.ingredient.price_per_unit * requirement.quantity

        context['total_cost'] = total_cost
        context['revenue'] = revenue
        context['profit'] = revenue - total_cost

        return context


class HomeView(TemplateView):
    template_name = 'inventory/home.html'


def logout_request(request):
    logout(request)
    return redirect("/")


def login_request(_):
    return redirect('/')
