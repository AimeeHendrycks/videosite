from django.db import models

# Create your models here.
from django.utils import timezone  
from django.utils.http import urlquote  
from django.core.mail import send_mail  
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class Movie(models.Model):

    class Meta:
        verbose_name_plural = "Movies"
        
    movie_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length = 255, null=True, blank=True, db_index=True)
    imdb_id = models.CharField(max_length = 255, null=True, blank=True)
    release_date = models.CharField(max_length = 255, null=True, blank=True)
    rating = models.CharField(max_length = 255, null=True, blank=True)
    artwork = models.CharField(max_length = 255, null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    trailer = models.CharField(max_length = 255, null=True, blank=True)
    upvote_count = models.IntegerField(default=0)
    downvote_count = models.IntegerField(default=0)
    


    def __unicode__(self):
        return self.title

class Show(models.Model):

    class Meta:
        verbose_name_plural = "Shows"

    show_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length = 255, null=True, blank=True, db_index=True)
    status = models.CharField(max_length = 255, null=True, blank=True)
    imdb_id = models.CharField(max_length = 255, null=True, blank=True)
    first_aired = models.CharField(max_length = 255, null=True, blank=True)
    rating = models.CharField(max_length = 255, null=True, blank=True)
    artwork = models.CharField(max_length = 255, null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    runtime = models.CharField(max_length = 255, null=True, blank=True)
    upvote_count = models.IntegerField(default=0)
    downvote_count = models.IntegerField(default=0)
    #episode list show.episode_set.all

    def __unicode__(self):
        return self.title

class Channel(models.Model):
    class Meta:
        verbose_name_plural = "Channels"

    channel_id = models.CharField(max_length = 255, null=True, blank=True)
    title = models.CharField(max_length = 255, null=True, blank=True, db_index=True)
    artwork = models.CharField(max_length = 255, null=True, blank=True)
    show = models.ManyToManyField(Show, blank=True)
    upvote_count = models.IntegerField(default=0)
    downvote_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


class Episode(models.Model):
    class Meta:
        verbose_name_plural = "Episodes"
        ordering = ['season_number', 'episode_number']

    title = models.CharField(max_length = 255, null=True, blank=True)
    episode_id = models.IntegerField(null=True, blank=True)
    imdb_id = models.CharField(max_length = 255, null=True, blank=True)
    season_number = models.IntegerField(null=True, blank=True)
    episode_number = models.IntegerField(null=True, blank=True)
    show = models.ForeignKey(Show, null=True, blank=True)
    first_aired = models.CharField(max_length = 255, null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    artwork = models.CharField(max_length = 255, null=True, blank=True)
    upvote_count = models.IntegerField(default=0, null=True)
    downvote_count = models.IntegerField(default=0, null=True)

    def __unicode__(self):
        return self.title


class Person(models.Model):
    person_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length = 255, null=True, blank=True)
    show = models.ManyToManyField(Show)
    episode = models.ManyToManyField(Episode)
    movie = models.ManyToManyField(Movie)

    def __unicode__(self):
        return unicode(self.name) or 'None'

class Actor(Person):
    class Meta:
        verbose_name_plural = "Actors"


class Writer(Person):
    class Meta:
        verbose_name_plural = "Writers"


class Director(Person):
    class Meta:
        verbose_name_plural = "Directors"

class VideoSource(models.Model):    
    display_name = models.CharField(max_length = 255, null=True, blank=True)
    source_link = models.CharField(max_length = 255, null=True, blank=True)
    episode = models.ForeignKey(Episode, null=True, blank=True)
    movie = models.ForeignKey(Movie, null=True, blank=True)

    def __unicode__(self):
        return self.display_name

class FreeSource(VideoSource):
    class Meta:
        verbose_name_plural = "Free Sources"


class TVSource(VideoSource):
    class Meta:
        verbose_name_plural = "TV Sources"

class SubSource(VideoSource):
    class Meta:
        verbose_name_plural = "Subscription Sources"

class PurchaseSource(VideoSource):
    #episode = models.ForeignKey(Episode, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Purchase Sources"

class CustomUserManager(BaseUserManager):  
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          last_login=now,
                          date_joined=now,
                          **extra_fields
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

class Color(models.Model):
    hex_value = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.title

class CustomUser(AbstractBaseUser, PermissionsMixin):  
    email = models.EmailField('email address', max_length=255, unique=True)
    first_name = models.CharField('first name', max_length=30, blank=True, null=True)
    last_name = models.CharField('last name', max_length=30, blank=True, null=True)
    account_name = models.CharField('account name', max_length=255, blank=True, null=True)
    account_color = models.ForeignKey(Color, null=True)
    account_picture = models.TextField(null=True, default='http://rebelinc.tv/wp-content/uploads/2015/07/Generic-person-350x350.jpg', blank=True)
    movie = models.ManyToManyField(Movie)
    show = models.ManyToManyField(Show)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])


class Comment(models.Model):
    is_reply = models.BooleanField()
    user = models.ForeignKey(CustomUser, null=True, blank=True)
    text = models.TextField(null=False, blank=True)
    date_created = models.DateTimeField('date created', auto_now_add=True)
    movie = models.ForeignKey(Movie, null=True, blank=True)
    show = models.ForeignKey(Show, null=True, blank=True)
    episode = models.ForeignKey(Episode, null=True, blank=True)
    channel = models.ForeignKey(Channel, null=True, blank=True)
    def __unicode__(self):
        return self.text

class Response(models.Model):
    is_resp_to_reply = models.BooleanField()
    original_comment = models.ForeignKey(Comment, null=True, blank=True)
    user = models.ForeignKey(CustomUser, null=True, blank=True)
    text = models.TextField(null=False, blank=True)
    date_created = models.DateTimeField('date created', auto_now_add=True)
    movie = models.ForeignKey(Movie, null=True, blank=True)
    show = models.ForeignKey(Show, null=True, blank=True)
    episode = models.ForeignKey(Episode, null=True, blank=True)
    channel = models.ForeignKey(Channel, null=True, blank=True)
    def __unicode__(self):
        return self.text

class Reply(models.Model):
    original_response = models.ForeignKey(Response, null=True, blank=True)
    copy = models.ForeignKey(Comment, null=True, blank=True)
    user = models.ForeignKey(CustomUser, null=True, blank=True)
    text = models.TextField(null=False, blank=True)
    date_created = models.DateTimeField('date created', auto_now_add=True)
    movie = models.ForeignKey(Movie, null=True, blank=True)
    show = models.ForeignKey(Show, null=True, blank=True)
    episode = models.ForeignKey(Episode, null=True, blank=True)
    channel = models.ForeignKey(Channel, null=True, blank=True)
    def __unicode__(self):
        return self.text


class Vote(models.Model):
    vote_type = models.CharField(max_length = 255, null=True, blank=True)
    user = models.ForeignKey(CustomUser, null=True, blank=True)
    movie = models.ForeignKey(Movie, null=True, blank=True)
    show = models.ForeignKey(Show, null=True, blank=True)
    channel = models.ForeignKey(Channel, null=True, blank=True)
    episode = models.ForeignKey(Episode, null=True, blank=True)

