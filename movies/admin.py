from django.contrib import admin
from django.db.models import Count
# Register your models here.
from .models import Movie, Review, Report, TopReviewer
class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(Report)

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