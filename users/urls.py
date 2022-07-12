
from django.urls import path
from .views import Register, login, current_user, LogoutView, bookCreate, bookUpdate, bookborrow, bookreturn
from . import views
from .models import User
from .serializers import RegisterSerializer


urlpatterns = [

    path('register', Register.as_view(), name='register'),
    path('login', login.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('current_user', views.current_user, name="current_user"),
   	path('book-list', views.bookList, name="book-list"),
   	path('book-detail/<str:pk>  /', views.bookDetail, name="book-detail"),
   	path('book-create', bookCreate.as_view(), name="book-create"),
    path('book-update/<str:pk> /', bookUpdate.as_view(), name="book-update"),
   	path('book-delete/<str:pk>/', views.bookDelete, name="task-delete"),
    path('book-borrow/<str:pk>/', views.bookborrow, name="book-borrow"),
    path('book-return/<str:pk>/', views.bookreturn, name="book-return"),

]
