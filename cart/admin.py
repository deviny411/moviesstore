from django.contrib import admin
from django.db.models import Sum
from django.http.request import HttpRequest

# Register your models here.
from .models import Order, Item, TopPurchaser, ListTopPurchasers
admin.site.register(Order)
admin.site.register(Item)

class TopPurchaserAdmin(admin.ModelAdmin):
    list_display = ['username', 'movies_purchased']
    def get_queryset(self, request):
        users = TopPurchaser.objects.all()
        users = users.annotate(movies_purchased=Sum('order__item__quantity'))
        users = users.exclude(movies_purchased = None)
        top = users.order_by('-movies_purchased').first()
        if top:
            users = users.filter(movies_purchased = top.movies_purchased)
        return users

    def movies_purchased(self, obj):
        return obj.movies_purchased

admin.site.register(TopPurchaser, TopPurchaserAdmin)

@admin.register(ListTopPurchasers)
class ListTopPurchasterAdmin(admin.ModelAdmin):
    list_display = ['username', 'movies_purchased']
    search_fields = ['username']
    def get_queryset(self, request):
        users = TopPurchaser.objects.all()
        users = users.annotate(movies_purchased=Sum('order__item__quantity'))
        users = users.exclude(movies_purchased = None)
        return users

    def movies_purchased(self, obj):
        return obj.movies_purchased
    
    def get_ordering(self, request):
        return ['-movies_purchased']
    
    def get_search_results(self, request, queryset, search_term):
        if search_term != "" and int(search_term) > 0:
            users = queryset.order_by('-movies_purchased')[0:int(search_term)]
            ids = list(users.values_list('id', flat=True))
            queryset = queryset.filter(id__in=ids)
        return queryset, False