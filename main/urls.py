from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('delete/<int:pk>/', views.delete_purchase, name='delete_purchase'),
    path('edit-price/<int:stock_id>/', views.edit_current_price, name='edit_current_price'),
    path('report/', views.portfolio_report, name='portfolio_report'),

]
