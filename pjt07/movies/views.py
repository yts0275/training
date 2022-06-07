from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Comment
from .forms import MovieForm, CommentForm

# Create your views here.
def index(request):
    movies = Movie.objects.all()

    context = {
        "movies": movies,
    }

    return render(request, "movies/index.html", context)


def create(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user_id = request.user
            movie.save()
            return redirect("movies:detail", movie.id)
    else:
        form = MovieForm()

    context = {
        'form': form,
    }

    return render(request, "movies/create.html", context)


def detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    comments = movie.comment_set.all()
    form = CommentForm()

    context = {
        'movie': movie,
        'comments': comments,
        'form': form,
    }

    return render(request, "movies/detail.html", context)


def update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user_id = request.user
            movie.save()
            return redirect("movies:detail", movie.id)
    else:
        form = MovieForm(instance=movie)

    context = {
        'movie': movie,
        'form': form,
    }

    return render(request, "movies/update.html", context)


def delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if movie.user_id == request.user:
        movie.delete()
        return redirect("movies:index")
    return redirect("movies:detail", movie.id)


def comments_create(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.movie_id = movie
            comment.user_id = request.user
            comment.save()
            return redirect("movies:detail", movie.id)


def comments_delete(request, movie_pk, comment_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    if comment.user_id == request.user:
        comment.delete()
        return redirect("movies:detail", movie.id)
    return redirect("movies:detail", movie.id)