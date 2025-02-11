from . import views
from django.urls import path

urlpatterns = [
    path("",views.home, name = "home"),
    path("filter/", views.dataRequest, name = "dataRequest"),
    path("submit-selection/", views.submitSelection, name = "submitSelection"),
    path('get-selected-items/', views.get_selected_items, name='get_selected_items'),
    path('clear-selection/', views.clear_selection, name='clear_selection'),
]