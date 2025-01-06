from django.contrib.auth.models import Group, User
from library_api.models import Books, BookRatings
from rest_framework import serializers

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'

class BookRatingsSerializer(serializers.ModelSerializer):
    class Meta:
        book_id = serializers.PrimaryKeyRelatedField(read_only=True)
        model = BookRatings
        fields = ['id','num_of_1_ratings' ,'num_of_2_ratings',
                  'num_of_3_ratings','num_of_4_ratings' ,
                  'num_of_5_ratings' ,'average_rating',
                  'total_num_of_ratings' ]

