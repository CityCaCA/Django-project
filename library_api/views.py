from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics, status
from django.db.models import F
from .models import Books, BookRatings
from .serializers import BooksSerializer, BookRatingsSerializer
from library_api.forms import BookCreationForm, BookUpdateForm




api_view(['GET','POST'])
def home_view(request):
    """
        This view returns home view regardless of the request 
        type
    """
    return render(request,"home.html")

@api_view(['GET','POST'])
def get_book_view(request):
     if request.method == "GET":
        return render(request,"get_books.html")
     if request.method == "POST":
        pk = request.POST.get('pk')
        return redirect('books', pk=pk)
     
@api_view(['GET'])
def book_view(request,pk):
    """
        This view returns book based on the primary key in the request parameter.

        If not, show a book's unavailable button(that can't post a request)

        Otherwise render the button as signin to reserve book regardless of book availabilty

        have the ratings button faded out if the user is not signed in,
        if they are with permissions to rate the books
        

    """
    book = Books.objects.filter(id=pk)
    if book:
            book = Books.objects.get(id=pk)
            book_ratings = BookRatings.objects.get(book_id=book)
            serialized_book = BooksSerializer(book).data
            serialized_book_ratings = BookRatingsSerializer(book_ratings).data
            context = {
                'book': serialized_book,
                'book_ratings': serialized_book_ratings
                    }
            
            return Response(context, status=status.HTTP_200_OK)
    else:
            context={"message": "Book not in database!"}
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        # pass in the Book object with the all the details
        # return rendering form
 
        # get book if id's valid,
        # pass in the Book object with the all the details
        # return rendering form
    
 
 # Querys

class BookListAPIView(generics.ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer

    def get(self,request, format=None):
        title = request.query_params.get("title","")

        if title:
            queryset = Books.objects.filter(title_icontains=title)
        else:
            queryset = Books.objects.all()
        serializer = BooksSerializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET','POST'])
def get_book_to_update_view(request):
  if request.method == "GET":
        return render(request,"get_book_to_update.html")
  if request.method == "POST":
        pk = request.POST.get('pk')
        return redirect('update_book', pk=pk) 
  
@api_view(['GET','POST'])
def get_book_to_rate_view(request):
  if request.method == "GET":
        return render(request,"get_book_to_rate.html")
  if request.method == "POST":
        pk = request.POST.get('pk')
        rating_value = request.POST.get('rating_value')
        return redirect('rate_book', pk=pk, rating_value=rating_value) 

@api_view(['GET','POST'])
def get_book_to_delete_view(request):
  if request.method == "GET":
        return render(request,"get_book_to_delete.html")
  if request.method == "POST":
        pk = request.POST.get('pk')
        return redirect('delete_book', pk=pk) 

@api_view(['GET','POST'])
def get_book_to_reserve_view(request):
  if request.method == "GET":
        return render(request,"get_book_to_reserve.html")
  if request.method == "POST":
        pk = request.POST.get('pk')
        return redirect('reserve_book', pk=pk)
  
@api_view(['GET','POST'])
def get_book_to_unreserve_view(request):
    if request.method == "GET":
        return render(request,"get_book_to_unreserve.html")
    if request.method == "POST":
        pk = request.POST.get('pk')
        return redirect('unreserve_book', pk=pk)

@api_view(['POST']) 
def reserve_book_view(request,pk):
    """
        This view processes a query to change a given books available
        to False
    """
    if Books.objects.filter(id=pk).exists():
        book =  Books.objects.get(id=pk)
    if book.is_reserved == False:
        book.is_reserved = True
        book.save()
        serialized_book = BooksSerializer(book).data
        context = {
            'message': 'This book is has been reserved!',
            'book': serialized_book
        }
        return Response(context, status.HTTP_200_OK)
    else:
        context = {
            'message': 'This book is unavailable!'
        }
        return Response(context, status.HTTP_405_METHOD_NOT_ALLOWED)
    
 
 # Querys

@api_view(['POST']) 
def unreserve_book_view(request,pk):
    """
        This view processes a query to change a given books available
        to True
    """
    if Books.objects.filter(id=pk).exists():
        book = Books.objects.get(id=pk)
    if book.is_reserved == True:
        book.is_reserved = False
        book.save()
        serialized_book = BooksSerializer(book).data
        context = {
            'message': 'This book is now available!',
            'book': serialized_book
        }
        return Response(context, status.HTTP_200_OK)
    else:
        context = {
            'message': 'This book is available!'
        }
        return Response(context, status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET','POST'])    
def add_book_view(request):
    """
        This view processes a request to add a book.
        if successful, the book is added to database.

        the validation for the route is:
        1.the user is signed with permissions to
        add the book,
        
        2. said book shouldnt also exist in the database.
        3. the title is unique and not None
        4. the isbn is unique and not None
        5. the author is not empty
        6. the image_url links to an image if not empty
        7. the date format is valid if not empty

    """

    if request.method == 'GET':
            form = BookCreationForm()
            return render(request, 'add_book.html', {'form': form})
    if request.method == 'POST':
            form = BookCreationForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                isbn = form.cleaned_data.get('isbn')
                isbn13 = form.cleaned_data.get('isbn13')
                author = form.cleaned_data.get('author')
                pub_year = form.cleaned_data.get('pub_year')
                image_url = form.cleaned_data.get('image_url')
                lang_code = form.cleaned_data.get('lang_code')
                book = Books.objects.create(title = title,
                                     isbn = isbn, 
                                     isbn13 =isbn13,
                                     author=author,
                                    pub_year=pub_year,
                                    image_url=image_url,
                                    lang_code=lang_code)
                serialized_book = BooksSerializer(book).data
               
                context = {'message':
                            'Book  object with ID: {0} and title {1} created!'.format(book.id, book.title),
                           'Updated': serialized_book}
                return Response(context,status=status.HTTP_201_CREATED)
            else:
                return render(request, 'add_book.html', {'form': form})

@api_view(['POST']) 
def delete_book_view(request,pk):
    """
        This view processes a request to delete a book.
        if successful, the book is removed from the database.

        the validation for the route is:
        1. The book is in the database

    """
    if request.method == 'POST':
        try:
                book = Books.objects.get(id=pk)
                title = book.title
                book.delete()
                context = {'message': 'Book with ID : {0} and title {1} Deleted!'.format(pk, title)}
                return Response( context,
                                status=status.HTTP_204_NO_CONTENT)
        except:
                context = {'message': 'Error book not in database!'}
                return Response(context, status=status.HTTP_404_NOT_FOUND)
 # Querys

@api_view(['GET','POST']) 
def update_book_view(request,pk):
    """
        This view processes a request to update the details on a book 
        within the database.
        if successful, the book is updated with the new information.

        the validation for the route is:
        1.the user is signed with permissions to
        update the book,
        
        2. said book should exist in the database.
        3. the author is not empty
        4. the date format is valid if not empty

        The books title and isbn cannot be edited

    """
    if Books.objects.filter(id=pk).exists():
        if request.method == 'GET':
                form = BookUpdateForm()
                return render(request, 'update_book.html', {'form': form, 'pk': pk})
        if request.method == 'POST':
                
                form = BookUpdateForm(request.POST)
                if form.is_valid():
                    book_before = book = Books.objects.get(id=pk)
                    isbn13 = form.cleaned_data.get('isbn13')
                    author = form.cleaned_data.get('author')
                    pub_year = form.cleaned_data.get('pub_year')
                    image_url = form.cleaned_data.get('image_url')
                    lang_code = form.cleaned_data.get('lang_code')
                    Books.objects.filter(id=pk).update(
                                        isbn13 =isbn13,
                                        author=author,
                                        pub_year=pub_year,
                                        image_url=image_url,
                                        lang_code=lang_code)
                    book_after = Books.objects.get(id=pk)
                    
                    serialized_book_before = BooksSerializer(book_before).data
                    serialized_book_after = BooksSerializer(book_after).data
                
                    context = {
                                'message':
                                'Book  object with ID: {0} and title {1} created!'.format(book.id, book.title),
                                'book_before': serialized_book_before,
                                'book_after': serialized_book_after,
                            }
                    return Response(context,status=status.HTTP_201_CREATED)
                else:
                    return render(request, 'update_book.html', {'form': form})
    else:
        context = {
            'message': 'Book with {0} ID does not exist in the Database!'
        }
        return Response(context,status=status.HTTP_404_NOT_FOUND)

@api_view(['POST']) 
def rate_book_view(request,pk,rating_value):
    """
        This view processes a request to update the ratings
        on a book with id

    """
    if request.method == 'POST':
        if Books.objects.filter(id=pk).exists():
            book = Books.objects.get(id=pk)
            rating_before =  BookRatings.objects.get(book_id=book)
            if rating_value == 5:
                BookRatings.objects.filter(book_id=book).update(num_of_5_ratings=F('num_of_5_ratings')+1)
            elif rating_value == 4:
                BookRatings.objects.filter(book_id=book).update(num_of_4_ratings=F('num_of_4_ratings')+1)
            elif rating_value == 3:
                BookRatings.objects.filter(book_id=book).update(num_of_3_ratings=F('num_of_3_ratings')+1)
            elif rating_value == 2:
                BookRatings.objects.filter(book_id=book).update(num_of_2_ratings=F('num_of_2_ratings')+1)
            elif rating_value == 1:
                BookRatings.objects.filter(book_id=book).update(num_of_1_ratings=F('num_of_1_ratings')+1)
            else:
                  context = {"message": "Value is out of range! Must be between 1 to 5! Value is {0}".format(rating_value)}
                  return Response(context,status=status.HTTP_405_METHOD_NOT_ALLOWED)
            rating_after =  BookRatings.objects.get(book_id=book)

            serialized_rating_before = BookRatingsSerializer(rating_before).data
            serialized_rating_after = BookRatingsSerializer(rating_after).data
            context = {
                 'ratings_before': serialized_rating_before,
                 'ratings_after': serialized_rating_after,
            }
            return Response(context,status=status.HTTP_200_OK)
        else:
            context = {
                'message': 'Book with {0} ID does not exist in the Database!'
            }
            return Response(context,status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        if Books.objects.filter(id=pk).exist():
            book =  Books.objects.filter(id=pk)
            book_rating = BookRatings.objects.filter(book_id=book)
            serialized_book = BooksSerializer(book).data
            serialized_book_rating = BookRatingsSerializer(book_rating).data
            context = {
                 "book": serialized_book,
                 "book_rating": serialized_book_rating
            }
