from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('',            views.login_view,    name='login'),
    path('login/',      views.login_view,    name='login'),
    path('logout/',     views.logout_view,   name='logout'),
    path('dashboard/',  views.dashboard,     name='dashboard'),

    # Customer
    path('showroom/',        views.showroom,       name='showroom'),
    path('review/',          views.review_view,    name='review'),
    path('review/thanks/',   views.review_success, name='review_success'),

    # Admin
    path('admin-panel/',                    views.admin_panel,    name='admin_panel'),
    path('vehicles/',                       views.manage_cars,    name='manage_cars'),
    path('vehicles/add/',                   views.add_car,        name='add_car'),
    path('vehicles/<int:pk>/edit/',         views.edit_car,       name='edit_car'),
    path('vehicles/<int:pk>/delete/',       views.delete_car,     name='delete_car'),
    path('reviews/',                        views.manage_reviews, name='manage_reviews'),
    path('reviews/<int:pk>/respond/',       views.add_comment,    name='add_comment'),
]
