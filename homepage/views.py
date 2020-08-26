from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse

from homepage.models import Author, Recipe
from homepage.forms import AddRecipeForm, AddAuthorForm, LoginForm


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
