

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import BookSerializer, RegisterSerializer, LoginSerializers
from .models import User, Book
import jwt
from knox.views import LoginView as KnoxLoginView
from .custompermission import Isadmin
from rest_framework.authtoken.serializers import AuthTokenSerializer
import datetime
from token import *
from rest_framework import generics, permissions
from knox.models import AuthToken
from rest_framework.decorators import api_view, permission_classes


class Register(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class login(generics.GenericAPIView):
    serializer_class = LoginSerializers

    def post(self, request, *args, **kwargs):
        permission_classes = (permissions.AllowAny,)

        serializer = self.get_serializer()
        serializer.book_id = request.data.get("email")
        serializer.bookname = request.data.get("password")
        if serializer.is_valid:
           

           return Response({"status": "Logged in Suceesfully"})


class LogoutView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class bookCreate(generics.GenericAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = BookSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Book added successfully")


class bookUpdate(APIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.book_id = request.data.get("book_id")
        instance.bookname = request.data.get("bookname")
        instance.bookstatus = request.data.get("bookname")
        instance.save()

        return Response("Book updated successfully")


@api_view(['PUT'])
def bookborrow(request, pk):

    book = Book.objects.get(id=pk)
    book.bookstatus = "Borrowed"
    book.save()

    return Response("Book borrowed successfully")


@api_view(['PUT'])
def bookreturn(request, pk):

    book = Book.objects.get(id=pk)
    book.bookstatus = "Available"
    book.save()

    return Response("Book Returned successfully")


@api_view(['GET'])
def current_user(request):
    serializer = RegisterSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([Isadmin])
def apiOverview(request):

    api_urls = {
        'createbook': '/createbook/',
        'updatebook': '/updatebook/',
        'deletebook': '/deletebook/', }

    return Response(api_urls)


@api_view(['GET'])
def bookList(request):
    book = Book.objects.all().order_by('book_id')
    serializer = BookSerializer(book, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def bookDetail(request, pk):
    book = Book.objects.get(id=pk)
    serializer = BookSerializer(book)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([Isadmin])
def bookDelete(request, pk):
    book = Book.objects.get(id=pk)
    book.delete()

    return Response('Item succsesfully delete!')
