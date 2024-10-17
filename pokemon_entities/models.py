from django.db import models  # noqa F401
from django.utils import timezone


class Pokemon(models.Model):
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='pokemon_pics/', blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, null=True, blank=True)
    lat = models.FloatField(verbose_name='latitude')
    lon = models.FloatField(verbose_name='longitude')
    appeared_at = models.DateTimeField(verbose_name='appearance date/time', blank=True, default=timezone.now)
    disappeared_at = models.DateTimeField(verbose_name='disappearance date/time', blank=True, null=True, default=None)


