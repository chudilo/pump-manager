from django.contrib import admin

from .models import Song, Mix, Version, Chart, Stage, Player

admin.site.register(Song)
admin.site.register(Mix)
admin.site.register(Version)
admin.site.register(Chart)
admin.site.register(Stage)
admin.site.register(Player)
# Register your models here.
