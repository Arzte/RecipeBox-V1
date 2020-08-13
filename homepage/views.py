from django.shortcuts import render, HttpResponseRedirect, reverse

from homepage.models import Author, Recipe
from homepage.forms import AddRecipeForm, AddAuthorForm


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


def add_recipe(request):
    if request.method == 'POST':
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get('title'),
                author=data.get('author'),
                description=data.get('description'),
                time_required=data.get('time_required'),
                instructions=data.get('instructions')
            )
        return HttpResponseRedirect(reverse("homepage"))

    form = AddRecipeForm()
    return render(request, 'generic_form.html', {
        "form": form,
        "name": "recipe"
    })


def add_author(request):
    if request.method == 'POST':
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data.get('name'),
                bio=data.get('bio')
            )
        return HttpResponseRedirect(reverse("homepage"))

    form = AddAuthorForm()
    return render(request, 'generic_form.html', {
        "form": form,
        "name": "author"
    })
