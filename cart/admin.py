from django.contrib import admin
from django.db.models import Sum

# Register your models here.
from .models import Order, Item, TopPurchaser
admin.site.register(Order)
admin.site.register(Item)

@admin.register(TopPurchaser)
class TopPurchaserAdmin(admin.ModelAdmin):
    list_display =  ['username', 'movies_purchased']
    def get_queryset(self, request):
        users = TopPurchaser.objects.all()
        users = users.annotate(movies_purchased=Sum('order__item__quantity'))
        users = users.exclude(movies_purchased=None)
        return users
    
    def movies_purchased(self, obj):
        return obj.movies_purchased

    def get_ordering(self, request):
        return ['-movies_purchased']