from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from accounts.models import User

# Create your models here.
class App(models.Model):
    app_id = models.AutoField(primary_key=True)
    app_name = models.CharField(max_length=100)
    size = models.CharField(max_length=20)
    version = models.CharField(max_length=20)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        'Category',
        on_delete = models.CASCADE,
    )
    developer = models.ForeignKey(
        'Developer',
        on_delete = models.CASCADE,
    )
    # device = models.ForeignKey(
    #     'Device',
    #     on_delete = models.CASCADE,
    # )
    
    reviewer = models.ManyToManyField(
        'Reviewer',
        through = 'Review', 
        related_name='from_reviewer',
    )
    language = models.ManyToManyField(
        'Language',
        through='App_to_language',
        related_name='from_language',
    )
    # Picture
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    def __str__(self):
        return self.app_name


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.category_name


class Developer(models.Model):
    developer_account = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=False)
    developer_id = models.AutoField(primary_key=True)
    developer_name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.developer_name



class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    stars = models.IntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(5)])
    # stars = models.DecimalField(max_digits=2, decimal_places=1, null=True)
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
    reviewer = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    review_count = models.IntegerField(default=0)
    app = models.ManyToManyField(
        'App', 
        through='Review',
        related_name='from_app'
    )
    def __str__(self):
        return self.reviewer.username


class Language(models.Model):
    language_id = models.AutoField(primary_key=True)
    language_name  = models.CharField(max_length=50, unique=True)
    app = models.ManyToManyField(
        'App',
        through='App_to_language',
        related_name='language_from_app',
    )
    def __str__(self):
        return self.language_name


class App_to_language(models.Model):
    id = models.AutoField(primary_key=True)
    app = models.ForeignKey(
        'App',
        on_delete = models.CASCADE,
    )
    language = models.ForeignKey(
        'Language',
        on_delete = models.CASCADE,
    )



# class Device(models.Model):
#     id = models.AutoField(primary_key=True)
#     device_name = models.CharField(max_length=50)
    
#     def __str__(self):
#         return self.device_name