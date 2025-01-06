from django.db import models
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
#from import_export import resources

# vlaidators for the book model
def validate_title_is_unique(title):
    if Books.objects.filter(title=title).exists():
        raise  ValidationError("title is already present in database!")

def validate_isbn_is_unique(isbn):
    # if null pass
    if isbn is not None :
        
        if Books.objects.filter(isbn=isbn).exists():
            raise  ValidationError("isbn is already present in database!")

def validate_isbn(isbn):
    # if null pass
    if isbn is not None :
        if len(isbn) >13:
            ValidationError("isbn is too long!")
        elif len(isbn) < 10:
            ValidationError("isbn is too short!")

  
# The Book Model
class BookManagerQuerySearch():
    def search_by_title():
        return
    
    def search_by_author():
        return
    
    def search_by_isbn():
        return
    
    def search_by_availability():
        return

class Books(models.Model):
    class Meta:
        verbose_name_plural = "Books"
        indexes = [models.Index(fields=['title'], name='title_idx')]
    id = models.BigAutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=100 , unique=True, null=False, validators=[validate_title_is_unique])
    isbn = models.CharField(max_length=100, null=True,validators=[validate_isbn_is_unique, validate_isbn])
    isbn13 = models.CharField(null=True, max_length=100)
    author = models.CharField(max_length=100, null=False)
    is_reserved = models.BooleanField(default=False)
    pub_year = models.DateField(null=True)
    image_url = models.CharField(max_length=200, null=True)
    lang_code = models.CharField(max_length=20,null=True)
    def __str__(self):
        return "Details ID : {0}, FK: {1}, year of publication {2}".format(self.id, self.book_id, self.pub_year)

    def save(self, *args, **kwargs):
         created = not self.pk
         super().save(*args, **kwargs)
         if created:
             BookRatings.objects.create(book_id=self)
    def __str__(self):
        return "Book: Id {0}, Title {1} ,Author: {2}, year of publication {3}, Is reserved {4}".format(self.id, self.title, self.author, self.pub_year,self.is_reserved)

 #Book Ratings

class BookRatings(models.Model):
    class Meta:
        verbose_name_plural = "BookRatings"
    id = models.BigAutoField(primary_key=True, auto_created=True)
    book_id  = models.OneToOneField(Books, on_delete=models.CASCADE)
    num_of_1_ratings = models.IntegerField(default=0)
    num_of_2_ratings = models.IntegerField(default=0)
    num_of_3_ratings = models.IntegerField(default=0)
    num_of_4_ratings = models.IntegerField(default=0)
    num_of_5_ratings = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    total_num_of_ratings = models.IntegerField(default=0)

    def get_average_rating(self):

        #error handling
        if self.total_num_of_ratings > 0:
            avg_rating = round((self.num_of_1_ratings+
                          2*self.num_of_2_ratings+
                          3*self.num_of_3_ratings +
                            4*self.num_of_4_ratings+
                            5*self.num_of_5_ratings)/self.total_num_of_ratings, 2)
        else: 
            avg_rating = 0
        return avg_rating
    
    def set_average_rating(self):
        self.average_rating = self.get_average_rating()  
         
    def __str__(self):
        return "Average Rating :  {0}, Total Ratings {1} ".format(self.get_average_rating(), self.total_num_of_ratings)
    

    
 



   

        



