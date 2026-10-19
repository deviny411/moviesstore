from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Report, Rating
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

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
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    reviewsReports = set()
    for review in reviews:
        reports = Report.objects.filter(review = review)
        if(len(reports) >0):
            reviewsReports.add(review.id)
    ratings = Rating.objects.filter(movie=movie)
    avarageRating = ratings.aggregate(Avg('stars'))['stars__avg']
    userRating = None
    userRatings = Rating.objects.filter(movie=movie, user=request.user.id)
    if len(userRatings) > 0:
        userRating = userRatings[0].stars
    
    

    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['reviewsReports'] = reviewsReports
    template_data['average_rating'] = avarageRating
    template_data['rating_count'] = len(ratings)
    template_data['user_rating'] = userRating
    return render(request, 'movies/show.html',
                  {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment']!= '':
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
def rate_movie(request, id):
    if request.method == 'POST' and request.POST['stars']!= '':
        movie = Movie.objects.get(id=id)
        userRatings = Rating.objects.filter(movie=movie, user=request.user)
        if len(userRatings) > 0:
            rating = userRatings[0]
        else:
            rating = Rating()
            rating.movie = movie
            rating.user=request.user
        rating.stars = int(request.POST['stars'])
        rating.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def report_review(request, id, review_id):
    movie = Movie.objects.get(id=id)
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST' and request.POST['comment']!= '':
        review = Review.objects.get(id=review_id)
        report = Report()
        report.comment = request.POST['comment']
        report.review = review

        report.user = request.user
        
        report.save()
        return redirect('movies.show', id=id)
    elif request.method == 'GET':
            template_data = {}
            template_data['review'] = review
            template_data['movie'] = movie
            return render(request, 'movies/report.html', {'template_data': template_data})
    else:
        return redirect('movies.show', id=id)