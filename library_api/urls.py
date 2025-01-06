"""
URL configuration for library_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
# from library_api.views import views
urlpatterns = [
    #schema routes
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'), # generates documentation for the api
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'), # visualises documentation for the api
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), # generates  more dynamics documentation for the api
    
    path('', views.home_view,name="home"),
    path('api/v1/books/', views.get_book_view, name="get_books"),
    path('api/v1/books/all', views.BookListAPIView.as_view(), name="book_list"),

    # Post views
    path('api/v1/books/<int:pk>', views.book_view, name="books"),
    path('api/v1/books/update_book/<int:pk>', views.update_book_view, name="update_book"),
    path('api/v1/books/delete_book/<int:pk>', views.delete_book_view, name="delete_book"),
    path('api/v1/books/<int:pk>/rate_book/<int:rating_value>', views.rate_book_view, name="rate_book"),
    path('api/v1/books/<int:pk>/reserve_book/', views.reserve_book_view, name="reserve_book"),
    path('api/v1/books/<int:pk>/unreserve_book/', views.unreserve_book_view, name="unreserve_book"),

    # Get and Post redirect views
    path('api/v1/books/add_book/', views.add_book_view, name="add_book"),
    path('api/v1/books/update_book/', views.get_book_to_update_view, name="get_book_to_update"),
    path('api/v1/books/delete_book/', views.get_book_to_delete_view, name="get_book_to_delete"),
    path('api/v1/books/rate_book/', views.get_book_to_rate_view, name="get_book_to_rate"),
    path('api/v1/books/reserve_book/', views.get_book_to_reserve_view, name="get_book_to_reserve"),
    path('api/v1/books/unreserve_book/', views.get_book_to_unreserve_view, name="get_book_to_unreserve"),
    
]
