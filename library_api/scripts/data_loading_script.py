# python Imports
import pandas as pd
import library_api.data.get_books_path as get_path
from datetime import datetime
# # Django imports
#from models import BooksResources, BookDetailsResources, BookRatingsResources
from library_api.models import Books,BookRatings
from django.db import transaction
#---------------------------


# reading the csv file
def run():
        DATA_CSV = get_path.get_books_path()+"\\books.csv"
        print(DATA_CSV)
        df = pd.read_csv(DATA_CSV)
        df = df.drop(columns=['goodreads_book_id', 'best_book_id', "title", 'work_id', 'ratings_count', 'books_count', 'small_image_url' , 'work_text_reviews_count'])
        df.rename(columns={'work_ratings_count': 'rating_count', 'original_title': 'title'}, inplace=True)
        # To get the accuaracy of the work ratings we need to drop the ratings_count and use the work_ratings_count column instead
        df.head()

        #---------------------------
        # Cleaning the data

        # printing the column names
        print(df.columns)

        # checking the number of rows
        print ("Number of rows before data cleaning: {}".format(df.shape[0])) # exactly 10,000 rows

        #checking the data types
        #print(df.dtypes)

        # checking for unique columns and for empty or nan rows
        df.dropna(how='any',axis=0, inplace=True)
        df = df.drop_duplicates(subset=['title'], keep='first')
        df = df.drop(df[df['original_publication_year'] < 0].index)

        #turning strings into integers
        df['book_id'] = pd.to_numeric(df['book_id'])

        
        # standizing the language codes or 'en-CA', 'en-CA',

        print("Unique language codes before standardisation: {0}".format(df['language_code'].unique()))

        df.loc[df.language_code == 'en-US' , 'language_code'] = 'eng'
        df.loc[df.language_code == 'en-CA' , 'language_code'] = 'eng'
        df.loc[df.language_code == 'en-GB' , 'language_code'] = 'eng'

        print("Unique language codes after standardisation: {0}".format(df['language_code'].unique()))


        # only uncomment to view details
        # print (df.shape[0])
        # for col in df:
        #     print('For the column {0} , it is {1} that the values are unique'.format(col, df[col].is_unique) )
        #     print('For the column {0} , it is {1} that the values are duplicated'.format(col, df[col].duplicated().any()) )


        print ("Number of rows after data cleaning: {0}".format(df.shape[0])) # only 7680 rows now

        #---------------------------
        # The list of column headers each Django model receives

        # Books
        #['book_id', 'isbn', 'isbn13', 'title','authors' ]


        # Book details
        #['book_id','original_publication_year',
        # 'language_code', 'image_url' ]

        # ratings
        #['book_id','average_rating',
        # 'rating_count', 'ratings_1', 
        # 'ratings_2', 'ratings_3', 'ratings_4','ratings_5' ]]

        #Importing the data:

        with transaction.atomic():
                book_list = []
                for index, row in df.iterrows():
                        book = Books(
                        id=row['book_id'],
                        title=row['title'],
                        isbn=row['isbn'],
                        isbn13=row['isbn13'],
                        author=row['authors'],
                        pub_year= datetime(int(row['original_publication_year']), 1, 1),
                        lang_code=row['language_code'],
                        image_url=row['image_url'])
                        
                        book_list.append(book)
                Books.objects.bulk_create(book_list)

                print("Finished Book data loading")
                       

                book_ratings_list = []
                for index,row in df.iterrows():
                        book_rating = BookRatings(
                        book_id = Books.objects.get(id=row['book_id']),
                        num_of_1_ratings= row['ratings_1'],
                        num_of_2_ratings=row['ratings_2'],
                        num_of_3_ratings=row['ratings_3'],
                        num_of_4_ratings=row['ratings_4'],
                        num_of_5_ratings=row['ratings_5'],
                        average_rating = row['average_rating'],
                        total_num_of_ratings=row['rating_count']
                        )
                        book_ratings_list.append(book_rating)
                BookRatings.objects.bulk_create(book_ratings_list)
                print("Finished Book ratings loading")

        print("Data has been loaded into the Django database.")
