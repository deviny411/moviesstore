from django.contrib import admin
from django.db.models import Count, Sum
from django.shortcuts import render

# Register your models here.
from .models import Movie, Review, Report, TopReviewer, Rating, MostPopularMovie
class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(Report)
admin.site.register(Rating)

@admin.register(TopReviewer)
class TopReviewerAdmin(admin.ModelAdmin):
    list_display =  ['username', 'reviews_made']
    def get_queryset(self, request):
        users = TopReviewer.objects.all()
        users = users.annotate(reviews_made=Count('review'))
        users = users.exclude(reviews_made=0)
        return users
    
    def reviews_made(self, obj):
        return obj.reviews_made

    def get_ordering(self, request):
        return ['-reviews_made']

@admin.register(MostPopularMovie)
class PopularMovieAdmin(admin.ModelAdmin):
    def changelist_view(self, request):
        mostBought = Movie.objects.annotate(x=Sum('item__quantity'))
        mostBought = mostBought.exclude(x=None).order_by('-x').first()

        mostReviewed = Movie.objects.annotate(x=Count('review'))
        mostReviewed = mostReviewed.exclude(x=0).order_by('-x').first()

        context = dict(
            self.admin_site.each_context(request),
            title = 'Most Popular Movie',
            mostBought=mostBought,
            mostReviewed=mostReviewed,
        )

        return render(request, 'admin/popularity.html', context)
    
    def get_queryset(self, request):
        users = TopReviewer.objects.all()
        users = users.annotate(reviews_made=Count('review'))
        users = users.exclude(reviews_made=0)
        return users
    
    def reviews_made(self, obj):
        return obj.reviews_made

    def get_ordering(self, request):
        return ['-reviews_made']
