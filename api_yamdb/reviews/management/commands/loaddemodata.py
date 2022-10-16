from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load demo data to database from static/data folder'

    def handle(self, *args, **options):
        call_command('makemigrations')
        call_command('migrate')
        call_command(
            'loadcsv',
            'static/data/users.csv',
            'authentication',
            'User'
        )
        call_command(
            'loadcsv',
            'static/data/category.csv',
            'reviews',
            'Category',
        )
        call_command(
            'loadcsv',
            'static/data/genre.csv',
            'reviews',
            'Genre',
        )
        call_command(
            'loadcsv',
            'static/data/titles.csv',
            'reviews',
            'Title'
        )
        call_command(
            'loadcsv',
            'static/data/genre_title.csv',
            'reviews',
            'TitleGenre',
            resource_class='reviews.resources.TitleGenreResource'
        )
        call_command(
            'loadcsv',
            'static/data/review.csv',
            'reviews',
            'Review',
            resource_class='reviews.resources.ReviewResource'
        )
        call_command(
            'loadcsv',
            'static/data/comments.csv',
            'reviews',
            'Comment',
            resource_class='reviews.resources.CommentResource'
        )
