from ..models import Book, Author, Genre
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework import status, generics, filters
from rest_framework.response import Response
from ..serializers import BookSerializer, AuthorSerializer, GenreSerializer
from rest_framework.decorators import api_view
from ..serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle , ScopedRateThrottle
from .throttling import genreThrottle
from django_filters.rest_framework import DjangoFilterBackend



@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data = request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()
            data['username'] = account.username
            data['email'] = account.email
            
            token = Token.objects.create(user=account)
            data['token'] = token.key
            
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_200_OK)


class RetrieveUpdateDestroyAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            queryset = Book.objects.get(id=id)
            serialized_data = BookSerializer(queryset)
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({'error':"Book not found"}, status=status.HTTP_404_NOT_FOUND)


    def put(self, request, id):
        try:
            queryset = Book.objects.get(id=id)
            self.check_object_permissions(request, queryset)
            serialized_data = BookSerializer(queryset, data=request.data)
            if(serialized_data.is_valid()):
                serialized_data.save()
                return Response(serialized_data.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({'error':"Book not found"}, status=status.HTTP_404_NOT_FOUND)
        


    def delete(self, request, id):
        try:
            queryset = Book.objects.get(id=id)
            queryset.delete()
            return Response(status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({'error':"Book not found"}, status=status.HTTP_404_NOT_FOUND)
        
class BooksAuthorAPIView(APIView):

    throttle_classes = [UserRateThrottle,AnonRateThrottle]

    def get(self, request):
        queryset = Author.objects.all()
        serialized_data = AuthorSerializer(queryset, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AuthorSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FilterBooksAPIView(generics.ListAPIView):

    serializer_class = BookSerializer

    def get_queryset(self):
        # book_name = self.kwargs['bookname'] we will have to pass the book_name in url
        book_name = self.request.query_params.get('bookname', None)
        return Book.objects.filter(title = book_name)
    
class DjangoFilterBooksAPIView(generics.ListAPIView):

    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author__name']

    def get_queryset(self):
        return Book.objects.all()
    
class SearchBooksAPIView(generics.ListAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__name']





class BooksAPIView(APIView):

    # permission_classes = [IsAuthenticated]
    # throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return Book.objects.all()
    
    def get(self, request, id=None):

        if id:
            queryset = Book.objects.get(id=id)
            serialized_data = BookSerializer(queryset)
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        queryset = Book.objects.all()
        serialized_data = BookSerializer(queryset, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class GenreAPIView(APIView):

    # throttle_classes = [genreThrottle] instead of this use scope throttle class preventing the creation of extra throttling.py class
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'genre-scope'

    def get(self, request):
        try:
            queryset = Genre.objects.all()
            serialized_data = GenreSerializer(queryset, many=True)
            return Response(serialized_data.data ,status=status.HTTP_200_OK)
        except Genre.DoesNotExist:
            return Response({"error":"no book with this genere exists"})
    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
