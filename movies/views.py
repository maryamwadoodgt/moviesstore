from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required
from .models import Petition, PetitionVote
from django.contrib import messages

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term, is_hidden=False)
    else:
        movies = Movie.objects.filter(is_hidden=False)
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

# NEW CODE
def movie_list(request):
    movies = Movie.objects.filter(is_hidden=False)
    template_data = {'movies': movies, 'title': 'Movies'}
    return render(request, "movies/index.html", {'template_data': template_data})

def hidden_movies(request):
    movies = Movie.objects.filter(is_hidden=True)
    template_data = {'movies': movies, 'title': 'Hidden Movies'}
    return render(request, "movies/hidden_movies.html", {'template_data': template_data})

def hide_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.is_hidden = True
    movie.save()
    return redirect("movie_list")

def unhide_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.is_hidden = False
    movie.save()
    return redirect("hidden_movies")


# Petitions feature
def petition_list(request):
    petitions = Petition.objects.all().order_by('-created_at')
    return render(request, 'movies/petitions/list.html', {'petitions': petitions})


@login_required
def petition_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        if not title:
            messages.error(request, 'Title is required')
            return redirect('petitions.list')
        p = Petition.objects.create(title=title, description=description, created_by=request.user)
        return redirect('petitions.detail', petition_id=p.id)

    return render(request, 'movies/petitions/create.html')


@login_required
def petition_detail(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    user_vote = None
    if request.user.is_authenticated:
        try:
            user_vote = PetitionVote.objects.get(petition=petition, user=request.user)
        except PetitionVote.DoesNotExist:
            user_vote = None
    return render(request, 'movies/petitions/detail.html', {'petition': petition, 'user_vote': user_vote})


@login_required
def petition_vote(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    # only allow POST
    if request.method != 'POST':
        return redirect('petitions.detail', petition_id=petition.id)

    # choice param optional -- default to yes/affirmative
    choice = request.POST.get('choice', 'yes')
    affirmative = True if choice.lower() in ('yes', 'true', '1') else False

    vote, created = PetitionVote.objects.get_or_create(petition=petition, user=request.user, defaults={'choice': affirmative})
    if not created:
        # update existing vote
        vote.choice = affirmative
        vote.save()

    messages.success(request, 'Your vote has been recorded')
    return redirect('petitions.detail', petition_id=petition.id)
