from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Comment
from .forms import MovieForm, CommentForm

# Create your views here.
def index(request):
    movies = Movie.objects.all()

    context = {
        'movies': movies,
    }
    return render(request, "movies/index.html", context)


def create(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("movies:index")
    else:
        form = MovieForm()

    context = {
        'form': form,
    }

    return render(request, "movies/create.html", context)


def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    comments = movie.comment_set.all()
    form = CommentForm()

    context = {
        'movie': movie,
        'comments': comments,
        'form': form,
    }

    return render(request, "movies/detail.html", context)


def update(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == "POST":
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect("movies:detail", movie.id)
    else:
        form = MovieForm(instance=movie)

    context = {
        'movie': movie,
        'form': form,
    }

    return render(request, "movies/update.html", context)


def delete(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie.delete()
    return redirect("movies:index")


def comments_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.movie_id = movie
            comment.save()
            return redirect("movies:detail", movie.id)


def comments_delete(request, movie_pk, comment_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    comment.delete()
    return redirect("movies:detail", movie.id)