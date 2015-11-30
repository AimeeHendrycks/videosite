from django.contrib import admin
from main.models import  Vote, Color, Reply,Response, Comment, Episode, Show, Movie, Channel, VideoSource, FreeSource, TVSource, SubSource, PurchaseSource, Person, Actor, Writer, Director, CustomUser, CustomUserManager
# Register your models here.

class EpisodeAdmin(admin.ModelAdmin):
    search_fields = ['title']

class MovieAdmin(admin.ModelAdmin):
    search_fields = ['title']

class ShowAdmin(admin.ModelAdmin):
    search_fields = ['title']

class ChannelAdmin(admin.ModelAdmin):
    search_fields = ['title']

class VideoSourceAdmin(admin.ModelAdmin):
    search_fields = ['display_name']

class FreeSourceAdmin(admin.ModelAdmin):
    search_fields = ['display_name']

class SubSourceAdmin(admin.ModelAdmin):
    search_fields = ['display_name']

class TVSourceAdmin(admin.ModelAdmin):
    search_fields = ['display_name']

class PurchaseSourceAdmin(admin.ModelAdmin):
    search_fields = ['display_name']

class PersonAdmin(admin.ModelAdmin):
    search_fields = ['name']

class ActorAdmin(admin.ModelAdmin):
    search_fields = ['name']

class WriterAdmin(admin.ModelAdmin):
    search_fields = ['name']

class DirectorAdmin(admin.ModelAdmin):
    search_fields = ['name']

class ColorAdmin(admin.ModelAdmin):
    search_fields = ['title']

class VoteAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_display= ('user','vote_type')

admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Show, ShowAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(VideoSource, VideoSourceAdmin)
admin.site.register(FreeSource, FreeSourceAdmin)
admin.site.register(SubSource, SubSourceAdmin)
admin.site.register(TVSource, TVSourceAdmin)
admin.site.register(PurchaseSource, PurchaseSourceAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Writer, WriterAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(CustomUser)
admin.site.register(Comment)
admin.site.register(Response)
admin.site.register(Reply)
admin.site.register(Color, ColorAdmin)
admin.site.register(Vote, VoteAdmin)
