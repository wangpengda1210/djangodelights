from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path("ingredients/", views.IngredientsView.as_view(), name='ingredients'),
    path('ingredients/new', views.IngredientCreateView.as_view(), name='create_ingredient'),
    path('ingredients/<slug:pk>/update', views.IngredientUpdateView.as_view(), name='update_ingredient'),
    path('menu_items/', views.MenuItemsView.as_view(), name='menuitems'),
    path('menu_items/new', views.MenuItemCreateView.as_view(), name='create_menuitem'),
    path('purchases/', views.PurchasesView.as_view(), name='purchases'),
    path('purchases/new', views.PurchaseCreateView.as_view(), name='create_purchase'),
    path('reciperequirements/new', views.RecipeRequirementCreateView.as_view(), name='create_reciperequirement'),
    path('profit/', views.ProfitView.as_view(), name='profit'),
    path('', views.HomeView.as_view(), name='home'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/profile/', views.login_request),
    path('logout/', views.logout_request, name='logout'),
]
