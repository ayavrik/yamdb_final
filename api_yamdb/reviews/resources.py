from import_export import fields, resources, widgets

from .models import Comment, Genre, Review, Title, TitleGenre


class TitleGenreResource(resources.ModelResource):
    title = fields.Field(
        column_name='title_id',
        attribute='title',
        widget=widgets.ForeignKeyWidget(Title, 'id')
    )
    genre = fields.Field(
        column_name='genre_id',
        attribute='genre',
        widget=widgets.ForeignKeyWidget(Genre, 'id')
    )

    class Meta:
        model = TitleGenre


class ReviewResource(resources.ModelResource):
    title = fields.Field(
        column_name='title_id',
        attribute='title',
        widget=widgets.ForeignKeyWidget(Title, 'id')
    )
    pub_date = fields.Field(
        column_name='pub_date',
        attribute='pub_date',
        widget=widgets.DateTimeWidget(format='%Y-%m-%dT%H:%M:%S.%fZ')
    )

    class Meta:
        model = Review


class CommentResource(resources.ModelResource):
    review = fields.Field(
        column_name='review_id',
        attribute='review',
        widget=widgets.ForeignKeyWidget(Review, 'id')
    )
    pub_date = fields.Field(
        column_name='pub_date',
        attribute='pub_date',
        widget=widgets.DateTimeWidget(format='%Y-%m-%dT%H:%M:%S.%fZ')
    )

    class Meta:
        model = Comment
