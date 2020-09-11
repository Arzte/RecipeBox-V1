from django.db import models
from django.contrib.auth.models import User

"""
Author
- Name (CharField)
- Bio (TextField)
- User (OneToOneField -> User)

Recipe
- Title (CharField)
- Author (ForeignKey)
- Description (TextField)
- Time Required (CharField)
- Instructions (TextField)
"""


class Author(models.Model):
    name = models.CharField(max_length=80)
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_recipe = models.ManyToManyField(to="Recipe",
                                             related_name="Recipe_Favorites",
                                             symmetrical=False)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField()
    time_required = models.CharField(max_length=20)
    instructions = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.author.name}"


# class Favorite(models.Model):
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE)
#     is_favorite = models.BooleanField(default=False)
#     user_favorite = models.CharField(max_length=80)

#     def __str__(self):
#         return f"{self.recipe} - {self.is_favorite}"
