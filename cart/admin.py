from django.contrib import admin
from django.db.models import Sum

# Register your models here.
from .models import Order, Item, TopPurchaser
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
