from django.db import models
from django.utils.text import slugify


def generate_unique_slug(name):
    slug = slugify(name)
    unique_slug = slug
    num = 1
    while Phone.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{slug}-{num}'
        num += 1
    return unique_slug


class Phone(models.Model):
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    image = models.ImageField()
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField(max_length=250, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}: {self.price}, {self.release_date}'
