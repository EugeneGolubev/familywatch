from django.db import models
from django.utils import timezone


class Genre(models.Model):
    tmdb_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=80, unique=True)

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    class Type(models.TextChoices):
        MOVIE = "movie", "Movie"
        TV = "tv", "TV Show"

    type = models.CharField(max_length=10, choices=Type.choices)
    tmdb_id = models.PositiveIntegerField()
    tvmaze_id = models.PositiveIntegerField(null=True, blank=True)
    imdb_id = models.CharField(max_length=30, blank=True)
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True)
    overview = models.TextField(blank=True)
    poster_path = models.CharField(max_length=255, blank=True)
    backdrop_path = models.CharField(max_length=255, blank=True)
    release_date = models.DateField(null=True, blank=True)
    first_air_date = models.DateField(null=True, blank=True)
    source_status = models.CharField(max_length=80, blank=True)
    runtime = models.PositiveIntegerField(null=True, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("type", "tmdb_id")

    def __str__(self) -> str:
        return f"{self.title} ({self.type})"


class Season(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="seasons")
    season_number = models.PositiveIntegerField()
    name = models.CharField(max_length=255, blank=True)
    overview = models.TextField(blank=True)
    air_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("title", "season_number")


class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="episodes")
    episode_number = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    overview = models.TextField(blank=True)
    air_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("season", "episode_number")


class Person(models.Model):
    tmdb_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.name


class CastCredit(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="cast_credits")
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="cast_credits")
    character = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
