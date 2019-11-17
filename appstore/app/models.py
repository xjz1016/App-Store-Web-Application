from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class App(models.Model):
    app_id = models.AutoField(primary_key=True)
    app_name = models.CharField(max_length=100)
    size = models.CharField(max_length=20)
    version = models.CharField(max_length=20)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    category = models.ForeignKey(
        'Category',
        on_delete = models.CASCADE,
    )
    developer = models.ForeignKey(
        'Developer',
        on_delete = models.CASCADE,
    )
    # price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    reviewer = models.ManyToManyField(
        'Reviewer',
        related_name = 'Review', 
    )
    language = models.ManyToManyField(
        'Language',
        related_name='app_language'
    )
    def __str__(self):
        return self.app_name


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)
    def __str__(self):
        return self.category_name


class Developer(models.Model):
    developer_id = models.AutoField(primary_key=True)
    developer_name = models.CharField(max_length=50)
    def __str__(self):
        return self.developer_name



class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    stars = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    review_text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )
    app = models.ForeignKey(
        'App',
        on_delete = models.CASCADE,
    )
    reviewer = models.ForeignKey(
        'Reviewer',
        on_delete = models.CASCADE,
    )


class Reviewer(models.Model):
    reviewer_id = models.AutoField(primary_key=True)
    reviewer_name = models.CharField(max_length=50)
    review_count = models.IntegerField()
    app = models.ManyToManyField(
        'App', 
        related_name='Review',
    )
    def __str__(self):
        return self.reviewer_name


class Language(models.Model):
    language_id = models.AutoField(primary_key=True)
    language_name  = models.CharField(max_length=50)
    app = models.ManyToManyField(
        'App',
        related_name='app_language'
    )
    def __str__(self):
        return self.language_name