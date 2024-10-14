from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='pokemon_pics/', blank=True)

    def __str__(self):
        return self.title
