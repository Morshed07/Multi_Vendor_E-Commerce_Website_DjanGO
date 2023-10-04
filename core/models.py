from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
# Create your models here.


class Main_Category(models.Model):
    title = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = 'Main Categories'


    def __str__(self) -> str:
        return self.title

class Category(models.Model):
    cid = ShortUUIDField(
        length=12,
        max_length=20,
        prefix="cat",
        alphabet="abcdefg1234",
        unique = True
    )
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category')

    class Meta:
        verbose_name_plural = 'Categories'

    def category_image(self):
        return 


    def __str__(self) -> str:
        return self.title