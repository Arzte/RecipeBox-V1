from django.db import models

"""
Author
- Name (CharField)
- Bio (TextField)

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
