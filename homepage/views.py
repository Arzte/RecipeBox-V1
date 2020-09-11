from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from homepage.models import Author, Recipe
from homepage.forms import AddRecipeForm, AddAuthorForm, LoginForm


# Create your views here.
def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'index.html', {
        "hello": "Recipe Box",
        "recipes": recipes})


def recipe_detail(request, recipe_id):
    try:
        recipe = Recipe.objects.filter(id=recipe_id).first()
        favorites = [f for f in Author.objects.get(
            user=request.user).favorite_recipe.all()]

    except Exception:
        favorites = None

    return render(request, 'recipe_detail.html', {"recipe": recipe, "favorites": favorites})


def author_detail(request, author_id):
    author = Author.objects.filter(id=author_id).first()
    recipes = Recipe.objects.filter(author=author.id)

    favorites = [f for f in Author.objects.get(
        id=author_id).favorite_recipe.all()]

    return render(request, 'author_detail.html', {
        "author": author,
        "recipes": recipes,
        "favorites": favorites or None
    })


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get('title'),
                author=request.user.author,
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


@login_required
def edit_recipe(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        initial_data = recipe.__dict__

        form = AddRecipeForm(initial=initial_data)
        if request.method == "POST":

            form = AddRecipeForm(request.POST, initial=initial_data)

            if form.is_valid() and form.has_changed():
                data = form.cleaned_data

                for field, data in data.items():
                    setattr(recipe, field, data)

                recipe.save()

            return HttpResponseRedirect(reverse("recipedetail", args=[recipe_id]))

    except Exception:
        return HttpResponseRedirect(reverse("homepage"))
    return render(request, "recipe_form.html", {"form": form})


@login_required
def add_author(request):
    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    if request.method == 'POST':
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data.get('username'),
                password=data.get('password')
            )
            user.author = Author.objects.create(
                name=data.get('name'),
                bio=data.get('bio'),
                user=user
            )

            login(request, user)
            return HttpResponseRedirect(reverse("homepage"))

    form = AddAuthorForm()
    return render(request, 'generic_form.html', {
        "form": form,
        "name": "author"
    })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get(
                'username'), password=data.get('password'))
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse("homepage"))
                )

    form = LoginForm()
    return render(request, 'generic_form.html', {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))


@login_required
def add_favorite(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        author = request.user.author
        favorite = Author.objects.get(
            user=request.user).favorite_recipe.get(id=recipe_id)

    except ObjectDoesNotExist:
        favorite = None

    if not favorite:
        author.favorite_recipe.add(recipe)
        return HttpResponseRedirect(reverse("recipedetail", args=[recipe_id]))

    author.favorite_recipe.remove(recipe)

    return HttpResponseRedirect(reverse("recipedetail", args=[recipe_id]))
