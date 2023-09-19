from django.contrib import admin

from games.models import Game, MyUser, Transaction, Comment


admin.site.register(Game)
admin.site.register(MyUser)
admin.site.register(Transaction)
admin.site.register(Comment)
