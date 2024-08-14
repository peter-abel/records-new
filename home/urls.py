from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('',views.home, name='home' ),
    path('404/',views.sos, name='sos'),
    path('account/',views.account, name='account' ),
    path('wallet/',views.wallet, name='wall' ),
     path('export/',views.export_excel, name='excel' ),
    
    path('login/',views.login, name='login'),
     path('activate/',views.activate, name='activate'),
    path('notifications/',views.notifications, name='notifications' ),
    path('orders/',views.orders, name='orders' ),
    path('reset/',views.reset, name='reset' ),
   
    path('signup/',views.signup, name='signup' ),
    path('order-form/',views.form, name='form' ),
    path('new-edit/<int:id>',views.new_edit, name='edit' ),
    path('new-edit/',views.new_edit, name='edit' ),
    path('search-orders/', csrf_exempt(views.search_orders), name="search_orders")
   

    
    

]