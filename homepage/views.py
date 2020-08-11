from django.shortcuts import render

from homepage.models import Author, Recipe


# Create your views here.
def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'index.html', {
        "hello": "Recipe Box",
        "recipes": recipes})


def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.filter(id=recipe_id).first()
    return render(request, 'recipe_detail.html', {"recipe": recipe})


def author_detail(request, author_id):
    author = Author.objects.filter(id=author_id).first()
    recipes = Recipe.objects.filter(author=author.id).all()
    return render(request, 'author_detail.html', {
        "author": author,
        "recipes": recipes
    })
