from io import BytesIO

from PIL import Image
from django.core.files.images import ImageFile
from django.db import models
from django.core.files import File


class Ingredients(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Cuisine(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='cuisine_images/')

    def __str__(self):
        return self.name
class Recipes(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='images/',blank = True,null = True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ingredients = models.ManyToManyField(Ingredients, related_name='recipes',blank=True)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, null=True, blank=True, related_name='recipes')
    ai_generated = models.BooleanField(default=False)

    class Meta:
        ordering = ('-updated_at',)

    def __str__(self):
        return self.title

    # def get_cuisine_by_name(self, name):
    #     return Cuisine.objects.get(name=name)
    #
    # def save(self, *args, **kwargs):
    #     if not self.image and self.cuisine:
    #         if isinstance(self.cuisine, str):
    #             self.cuisine = self.get_cuisine_by_name(self.cuisine)
    #         if self.cuisine.image:
    #             self.image = self.cuisine.image
    #     super().save(*args, **kwargs)
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self,image):
        if not image:
            return ''
        with Image.open(image) as img:
            max_size = (300, 300)
            img.thumbnail(max_size)
            thumb_io = BytesIO()
            img.save(thumb_io, 'JPEG')
            thumbnail_name = f"thumbnail_{self.image.name}"
            thumbnail = ImageFile(thumb_io, name=thumbnail_name)
            return thumbnail

