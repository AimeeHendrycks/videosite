from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from main.models import Vote, Movie, Show, Episode, Channel, Person, CustomUser, CustomUserManager, Comment, Response, Reply
from main.forms import UserSignUp, UserLogin, CommentForm, ResponseForm
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

def base(request):
    context = {}
    return render_to_response('base.html', context, context_instance=RequestContext(request))   

def please_login(request):
    context = {}
    return render_to_response('please_login.html', context, context_instance=RequestContext(request))   

def signup(request):

    context = {}

    form = UserSignUp()
    context['form'] = form

    if request.method == 'POST':
        form = UserSignUp(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                new_user = CustomUser.objects.create_user(email, password)
                                
                auth_user = authenticate(email=email, password=password)
                login(request, auth_user)
                return HttpResponseRedirect('/please_login/')

            except IntegrityError, e:
                context['valid'] = "A User With That Name Already Exists"

        else:
            context['valid'] = form.errors

    return render_to_response('signup.html', context, context_instance=RequestContext(request))

def login_view(request):
    context = {}
    form = UserLogin()
    context['form'] = form

    if request.method == 'POST':
        form = UserLogin(request.POST)
        context['form'] = form
        print "validating"
        if form.is_valid():
            print "am i valid?"

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            auth_user = authenticate(email=email, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return HttpResponseRedirect('/')
            else:
                context['valid'] = "Invalid User"
        else:
            context['valid'] = "Please enter an Email and Password"
    else:
        print 'GET'

    return render_to_response('login.html', context, context_instance=RequestContext(request))


def logout_view(request):

    logout(request)

    return HttpResponseRedirect('/login/')

def profile(request, pk):
    context = {}
    print pk
    num = int(pk)
    print num
    print request.user.pk
    if request.user.pk == num:
        print 'Yay!'
        context['user'] = request.user
        return render_to_response('profile.html', context, context_instance=RequestContext(request))
    else:
        print 'No!'
        return redirect('/')

class ProfileUpdate(UpdateView):
    model = CustomUser
    template_name = 'profile_update.html'
    fields = ['account_name', 'account_color', 'account_picture']
    success_url = '/'

def home(request):
    context = {}
    #making sure the images are loaded
    context['shows'] = Show.objects.filter(artwork__icontains='h').order_by('?')[:6]
    context['movies'] = Movie.objects.filter(artwork__icontains='h').order_by('?')[:6]
    context['channels'] = Channel.objects.all()
    return render_to_response('home.html', context, context_instance=RequestContext(request))


class ChannelSearch(ListView):
    model = Channel
    template_name = 'channel_search.html'
    paginate_by =24
    def get_queryset(self):
        object_list = []
        if 'search' in self.request.GET:
            object_list = Channel.objects.filter(title__icontains=self.request.GET['search'])
        else:
            object_list = Channel.objects.all()
        print object_list
        return object_list

class ChannelDetail(DetailView):
    model = Channel
    template_name = 'channel_detail.html'

class ChannelCreate(CreateView):
    model = Channel
    template_name = 'channel_create.html'
    fields = ['title', 'artwork']
    success_url = '/channel_search/'

class ChannelUpdate(UpdateView):
    model = Channel
    template_name = 'channel_update.html'
    fields = ['title', 'artwork']
    success_url = '/channel_search/'

class ChannelDelete(DeleteView):
    model = Channel
    template_name = 'channel_delete.html'
    success_url = '/channel_search/'

class MovieSearch(ListView):
    model = Movie
    template_name = 'movie_search.html'
    paginate_by =24
    def get_queryset(self):
        object_list = []
        if 'search' in self.request.GET:
            object_list = Movie.objects.filter(title__icontains=self.request.GET['search'])
        else:
            object_list = list(Movie.objects.raw('SELECT main_movie.id, main_movie.artwork, main_movie.upvote_count, main_movie.downvote_count, main_movie.title FROM main_movie'))
        print object_list
        return object_list

def movie_detail(request, pk):
    context = {}
    movie = Movie.objects.get(pk=pk)
    context['movie'] = movie
    context['imdb'] = 'http://www.imdb.com/title/' + str(movie.imdb_id)
    context['form1'] = CommentForm()
    if request.method == 'POST':
        form1 = CommentForm(request.POST)
        context['form1'] = form1
        if form1.is_valid():
            print 'valid form1'
            print request.user
            if request.user.is_authenticated():
                print 'comment'
                new_comment = Comment()
                new_comment.is_response = False
                new_comment.text = form1.cleaned_data['text']  
                new_comment.user = request.user
                new_comment.movie = movie
                new_comment.save()
                return HttpResponseRedirect('/movie_detail/%s' %pk )       
            else:  
                print 'anonymous user'
                return HttpResponseRedirect('/please_login/')
                
        else:
            print 'form1 not valid'
    else:
        print 'GET'
    return render_to_response('movie_detail.html', context, context_instance=RequestContext(request))

class MovieCreate(CreateView):
    model = Movie
    template_name = 'movie_create.html'
    fields = ['title', 'artwork', 'imdb_id', 'release_date', 'rating', 'overview']
    success_url = '/movie_search/'

class MovieUpdate(UpdateView):
    model = Movie
    template_name = 'movie_update.html'
    fields = ['title', 'artwork', 'imdb_id', 'release_date', 'rating', 'overview']
    success_url = '/movie_search/'

class MovieDelete(DeleteView):
    model = Movie
    template_name = 'movie_delete.html'
    success_url = '/movie_search/'


class ShowSearch(ListView):
    model = Show
    template_name = 'show_search.html'
    paginate_by =24
    def get_queryset(self):
        object_list = []
        if 'search' in self.request.GET:
            object_list = Show.objects.filter(title__icontains=self.request.GET['search'])
        else:
            object_list = list(Show.objects.raw('SELECT main_show.id, main_show.artwork, main_show.upvote_count, main_show.downvote_count, main_show.title FROM main_show'))
        print object_list
        return object_list

def show_detail(request, pk):
    context = {}
    show = Show.objects.get(pk=pk)
    context['form'] = CommentForm()
    context['show'] = show
    context['imdb'] = 'http://www.imdb.com/title/' + str(show.imdb_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        context['form'] = form
        if form.is_valid():
            if request.user.is_anonymous:
                print 'anonymous user'
                return HttpResponseRedirect('/please_login/')
            else:
                new_comment = Comment()
                new_comment.text = form.cleaned_data['text']
                new_comment.user = request.user
                new_comment.show = show
                new_comment.save()
                return HttpResponseRedirect('/show_detail/%s' %pk )
            
        else:
            print 'form not valid'
    return render_to_response('show_detail.html', context, context_instance=RequestContext(request))


class ShowCreate(CreateView):
    model = Show
    template_name = 'show_create.html'
    fields = ['title', 'status', 'artwork', 'imdb_id', 'first_aired', 'rating', 'overview', 'runtime']
    success_url = '/show_search/'

class ShowUpdate(UpdateView):
    model = Show
    template_name = 'show_update.html'
    fields = ['title', 'status', 'artwork', 'imdb_id', 'first_aired', 'rating', 'overview', 'runtime']
    success_url = '/show_search/'

class ShowDelete(DeleteView):
    model = Show
    template_name = 'show_delete.html'
    success_url = '/show_search/'


class EpisodeSearch(ListView):
    model = Episode
    template_name = 'episode_search.html'
    paginate_by =24
    def get_queryset(self):
        object_list = []
        if 'search' in self.request.GET:
            object_list = Episode.objects.filter(title__icontains=self.request.GET['search'])
        else:
            object_list = Episode.objects.all()
        print object_list
        return object_list

def episode_detail(request, pk):
    context = {}
    episode = Episode.objects.get(pk=pk)
    context['form'] = CommentForm()
    context['episode'] = episode
    context['imdb'] = 'http://www.imdb.com/title/' + str(episode.imdb_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        context['form'] = form
        if form.is_valid():
            if request.user.is_authenticated:
                new_comment = Comment()
                new_comment.text = form.cleaned_data['text']
                new_comment.user = request.user
                new_comment.episode = episode
                new_comment.save()
            elif request.user.is_anonymous:
                print 'anonymous user'
                return HttpResponseRedirect('/please_login/')
            return HttpResponseRedirect('/episode_detail/%s' %pk )
            
        else:
            print 'form not valid'
    return render_to_response('episode_detail.html', context, context_instance=RequestContext(request))

class EpisodeCreate(CreateView):
    model = Episode
    template_name = 'episode_create.html'
    fields = ['title', 'artwork', 'imdb_id', 'first_aired', 'overview', 'season_number', 'episode_number']
    success_url = '/episode_search/'

class EpisodeUpdate(UpdateView):
    model = Episode
    template_name = 'episode_update.html'
    fields = ['title', 'artwork', 'imdb_id', 'first_aired', 'overview', 'season_number', 'episode_number']
    success_url = '/episode_search/'

class EpisodeDelete(DeleteView):
    model = Episode
    template_name = 'episode_delete.html'
    success_url = '/episode_search/'

class PersonSearch(ListView):
    model = Person
    template_name = 'person_search.html'
    paginate_by =24
    def get_queryset(self):
        object_list = []
        if 'search' in self.request.GET:
            object_list = Person.objects.filter(name__icontains=self.request.GET['search'])
        else:
            object_list = Person.objects.all()
        print object_list
        return object_list

class GeneralSearch(ListView):
    model = Movie
    template_name = 'general_search.html'
    def get_context_data(self, **kwargs):
            context = super(GeneralSearch, self).get_context_data(**kwargs)
            #movies
            if 'search' in self.request.GET:
                movie_list = Movie.objects.filter(title__icontains=self.request.GET['search'])[:12]
            else:
                movie_list = Movie.objects.all()[:12]
            context['movies'] = movie_list
            
            #shows
            if 'search' in self.request.GET:
                show_list = Show.objects.filter(title__icontains=self.request.GET['search'])[:12]
            else:
                show_list = Show.objects.all()[:12]
            context['shows'] = show_list

            # #episodes
            # if 'search' in self.request.GET:
            #     episode_list = Episode.objects.filter(title__icontains=self.request.GET['search'])[:15]
            # else:
            #     episode_list = Episode.objects.all()[:6]
            # context['episodes'] = episode_list

            #channels
            if 'channel' in self.request.GET:
                channel_list = Channel.objects.filter(title__icontains=self.request.GET['search'])[:12]
            else:
                channel_list = Channel.objects.all()[:12]
            context['channels'] = channel_list

            # #people
            # if 'search' in self.request.GET:
            #     person_list = Person.objects.filter(name__icontains=self.request.GET['search'])[:15]
            # else:
            #     person_list = Person.objects.all()[:12]
            # context['people'] = person_list

            return context

def add_show(request, pk):
    request.user.show.add(Show.objects.get(pk=pk))
    return HttpResponseRedirect('/profile/%s' % request.user.pk)

def remove_show(request, pk):
    request.user.show.remove(Show.objects.get(pk=pk))
    return HttpResponseRedirect('/profile/%s' % request.user.pk)


def add_movie(request, pk):
    request.user.movie.add(Movie.objects.get(pk=pk))
    return HttpResponseRedirect('/profile/%s' % request.user.pk)

def remove_movie(request, pk):
    request.user.movie.remove(Movie.objects.get(pk=pk))
    return HttpResponseRedirect('/profile/%s' % request.user.pk)

def remove_movie_comment(request, comment_pk, movie_pk):
    Comment.objects.get(pk=comment_pk).delete()
    return HttpResponseRedirect('/movie_detail/%s' %movie_pk)

def remove_movie_response(request, response_pk, movie_pk):
    Response.objects.get(pk=response_pk).delete()
    return HttpResponseRedirect('/movie_detail/%s' %movie_pk)

def remove_movie_reply(request, reply_pk, movie_pk):
    Reply.objects.get(pk=reply_pk).delete()
    return HttpResponseRedirect('/movie_detail/%s' %movie_pk)


def remove_show_comment(request, comment_pk, show_pk):
    Comment.objects.get(pk=comment_pk).delete()
    return HttpResponseRedirect('/show_detail/%s' %show_pk)

def remove_show_response(request, response_pk, show_pk):
    Response.objects.get(pk=response_pk).delete()
    return HttpResponseRedirect('/show_detail/%s' %show_pk)

def remove_show_reply(request, reply_pk, show_pk):
    Reply.objects.get(pk=reply_pk).delete()
    return HttpResponseRedirect('/show_detail/%s' %show_pk)


def remove_episode_comment(request, comment_pk, episode_pk):
    Comment.objects.get(pk=comment_pk).delete()
    return HttpResponseRedirect('/episode_detail/%s' %episode_pk)

def remove_episode_response(request, response_pk, episode_pk):
    Response.objects.get(pk=response_pk).delete()
    return HttpResponseRedirect('/episode_detail/%s' %episode_pk)

def remove_episode_reply(request, reply_pk, episode_pk):
    Reply.objects.get(pk=reply_pk).delete()
    return HttpResponseRedirect('/episode_detail/%s' %episode_pk)

def remove_channel_comment(request, comment_pk, channel_pk):
    Comment.objects.get(pk=comment_pk).delete()
    return HttpResponseRedirect('/channel_detail/%s' %channel_pk)

def remove_channel_response(request, response_pk, channel_pk):
    Response.objects.get(pk=response_pk).delete()
    return HttpResponseRedirect('/channel_detail/%s' %channel_pk)

def remove_channel_reply(request, reply_pk, channel_pk):
    Reply.objects.get(pk=reply_pk).delete()
    return HttpResponseRedirect('/channel_detail/%s' %channel_pk)




def commentmovie(request, pk):
    context = {}
    if request.user.is_authenticated():
        print 'comment'
        print request.GET.get('comment')
        new_comment = Comment()
        new_comment.is_reply = False
        new_comment.text = request.GET.get('comment')
        new_comment.user = request.user
        new_comment.movie = Movie.objects.get(pk=pk)
        new_comment.save()
        return HttpResponseRedirect('/movie_detail/%s' %pk)
   
    else:  
        print 'anonymous user'
        return HttpResponseRedirect('/please_login/')
    return render_to_response('movie_detail.html', context, context_instance=RequestContext(request))

def respondmovie(request, pk1, pk2, num):
    context = {}
    if request.user.is_authenticated():
        print 'response'
        print request.GET.get('response')
        new_response = Response() 
        print num
        if int(num) == 1:
            new_response.is_resp_to_reply = False
        else:
            new_response.is_resp_to_reply = True
        print  'New resp' + str(new_response.is_resp_to_reply)
        new_response.text = request.GET.get('response')
        new_response.movie = Movie.objects.get(pk=pk1)
        new_response.original_comment = Comment.objects.get(pk=pk2)
        new_response.user = request.user
        new_response.save()
        return HttpResponseRedirect('/movie_detail/%s' %pk1) 
   
    else:  
        print 'anonymous user'
        return HttpResponseRedirect('/please_login/')
    return render_to_response('movie_detail.html', context, context_instance=RequestContext(request))



def replymovie(request, pk1, pk2):
    context = {}
    if request.user.is_authenticated():
        print 'reply'
        print request.GET.get('reply')
        new_comment = Comment()
        new_comment.is_reply = True
        new_comment.text = request.GET.get('reply')
        new_comment.user = request.user
        new_comment.movie = Movie.objects.get(pk=pk1)
        new_comment.save()
        new_reply = Reply()    
        new_reply.text = request.GET.get('reply')
        new_reply.original_response = Response.objects.get(pk=pk2)
        new_reply.copy = new_comment
        new_reply.user = request.user
        new_reply.movie = Movie.objects.get(pk=pk1)
        new_reply.save()

        return HttpResponseRedirect('/movie_detail/%s' %pk1) 
   
    else:  
        print 'anonymous user'
        return HttpResponseRedirect('/please_login/')
    return render_to_response('movie_detail.html', context, context_instance=RequestContext(request))


def commentshow(request, pk):
    context = {}
    if request.user.is_authenticated():
        print 'comment'
        print request.GET.get('comment')
        new_comment = Comment()
        new_comment.is_reply = False
        new_comment.text = request.GET.get('comment')
        new_comment.user = request.user
        new_comment.show = Show.objects.get(pk=pk)
        new_comment.save()
        return HttpResponseRedirect('/show_detail/%s' %pk)
   
    else:  
        print 'anonymous user'
        return HttpResponseRedirect('/please_login/')
    return render_to_response('show_detail.html', context, context_instance=RequestContext(request))

def respondshow(request, pk1, pk2, num):
    context = {}
    if request.user.is_authenticated():
        print 'response'
        print request.GET.get('response')
        new_response = Response() 
        print num
        if int(num) == 1:
            new_response.is_resp_to_reply = False
        else:
            new_response.is_resp_to_reply = True
        print  'New resp' + str(new_response.is_resp_to_reply)
        new_response.text = request.GET.get('response')
        new_response.show = Show.objects.get(pk=pk1)
        new_response.original_comment = Comment.objects.get(pk=pk2)
        new_response.user = request.user
        new_response.save()
        return HttpResponseRedirect('/show_detail/%s' %pk1) 
   
    else:  
        print 'anonymous user'
        return HttpResponseRedirect('/please_login/')
    return render_to_response('show_detail.html', context, context_instance=RequestContext(request))



def replyshow(request, pk1, pk2):
    context = {}
    if request.user.is_authenticated():
        print 'reply'
        print request.GET.get('reply')
        new_comment = Comment()
        new_comment.is_reply = True
        new_comment.text = request.GET.get('reply')
        new_comment.user = request.user
        new_comment.show = Show.objects.get(pk=pk1)
        new_comment.save()
        new_reply = Reply()    
        new_reply.text = request.GET.get('reply')
        new_reply.original_response = Response.objects.get(pk=pk2)
        new_reply.copy = new_comment
        new_reply.user = request.user
        new_reply.show = Show.objects.get(pk=pk1)
        new_reply.save()

        return HttpResponseRedirect('/show_detail/%s' %pk1) 
   
    else:  
        print 'anonymous user'
        return HttpResponseRedirect('/please_login/')
    return render_to_response('show_detail.html', context, context_instance=RequestContext(request))


def commentepisode(request, pk):
    context = {}
    if request.user.is_authenticated():
        print 'comment'
        print request.GET.get('comment')
        new_comment = Comment()
        new_comment.is_reply = False
        new_comment.text = request.GET.get('comment')
        new_comment.user = request.user
        new_comment.episode = Episode.objects.get(pk=pk)
        new_comment.save()
        return HttpResponseRedirect('/episode_detail/%s' %pk)
   
    else:  
        print 'anonymous user'
        return HttpResponseRedirect('/please_login/')
    return render_to_response('episode_detail.html', context, context_instance=RequestContext(request))

def respondepisode(request, pk1, pk2, num):
    context = {}
    if request.user.is_authenticated():
        print 'response'
        print request.GET.get('response')
        new_response = Response() 
        print num
        if int(num) == 1:
            new_response.is_resp_to_reply = False
        else:
            new_response.is_resp_to_reply = True
        print  'New resp' + str(new_response.is_resp_to_reply)
        new_response.text = request.GET.get('response')
        new_response.episode = Episode.objects.get(pk=pk1)
        new_response.original_comment = Comment.objects.get(pk=pk2)
        new_response.user = request.user
        new_response.save()
        return HttpResponseRedirect('/episode_detail/%s' %pk1) 
   
    else:  
        print 'anonymous user'
        return HttpResponseRedirect('/please_login/')
    return render_to_response('episode_detail.html', context, context_instance=RequestContext(request))



def replyepisode(request, pk1, pk2):
    context = {}
    if request.user.is_authenticated():
        print 'reply'
        print request.GET.get('reply')
        new_comment = Comment()
        new_comment.is_reply = True
        new_comment.text = request.GET.get('reply')
        new_comment.user = request.user
        new_comment.episode = Episode.objects.get(pk=pk1)
        new_comment.save()
        new_reply = Reply()    
        new_reply.text = request.GET.get('reply')
        new_reply.original_response = Response.objects.get(pk=pk2)
        new_reply.copy = new_comment
        new_reply.user = request.user
        new_reply.episode = Episode.objects.get(pk=pk1)
        new_reply.save()

        return HttpResponseRedirect('/episode_detail/%s' %pk1) 
   
    else:  
        print 'anonymous user'
        return HttpResponseRedirect('/please_login/')
    return render_to_response('episode_detail.html', context, context_instance=RequestContext(request))


def commentchannel(request, pk):
    context = {}
    if request.user.is_authenticated():
        print 'comment'
        print request.GET.get('comment')
        new_comment = Comment()
        new_comment.is_reply = False
        new_comment.text = request.GET.get('comment')
        new_comment.user = request.user
        new_comment.channel = Channel.objects.get(pk=pk)
        new_comment.save()
        return HttpResponseRedirect('/channel_detail/%s' %pk)
   
    else:  
        print 'anonymous user'
        return HttpResponseRedirect('/please_login/')
    return render_to_response('channel_detail.html', context, context_instance=RequestContext(request))

def respondchannel(request, pk1, pk2, num):
    context = {}
    if request.user.is_authenticated():
        print 'response'
        print request.GET.get('response')
        new_response = Response() 
        print num
        if int(num) == 1:
            new_response.is_resp_to_reply = False
        else:
            new_response.is_resp_to_reply = True
        print  'New resp' + str(new_response.is_resp_to_reply)
        new_response.text = request.GET.get('response')
        new_response.channel = Channel.objects.get(pk=pk1)
        new_response.original_comment = Comment.objects.get(pk=pk2)
        new_response.user = request.user
        new_response.save()
        return HttpResponseRedirect('/channel_detail/%s' %pk1) 
   
    else:  
        print 'anonymous user'
        return HttpResponseRedirect('/please_login/')
    return render_to_response('channel_detail.html', context, context_instance=RequestContext(request))



def replychannel(request, pk1, pk2):
    context = {}
    if request.user.is_authenticated():
        print 'reply'
        print request.GET.get('reply')
        new_comment = Comment()
        new_comment.is_reply = True
        new_comment.text = request.GET.get('reply')
        new_comment.user = request.user
        new_comment.channel = Channel.objects.get(pk=pk1)
        new_comment.save()
        new_reply = Reply()    
        new_reply.text = request.GET.get('reply')
        new_reply.original_response = Response.objects.get(pk=pk2)
        new_reply.copy = new_comment
        new_reply.user = request.user
        new_reply.channel = Channel.objects.get(pk=pk1)
        new_reply.save()

        return HttpResponseRedirect('/channel_detail/%s' %pk1) 
   
    else:  
        print 'anonymous user'
        return HttpResponseRedirect('/please_login/')
    return render_to_response('channel_detail.html', context, context_instance=RequestContext(request))

def vote_movie(request, pk, num):
    context = {}
    if request.user.is_authenticated():
        if int(num) == 1:
            vote_type = 'up'
        elif int(num) == 2:
            vote_type = 'down'
        movie = Movie.objects.get(pk=pk)
        new_vote, created = Vote.objects.get_or_create(user=request.user, movie=movie)
        new_vote.vote_type = vote_type
        new_vote.save()

        movie.upvote_count = movie.vote_set.filter(vote_type = 'up').count()
        movie.downvote_count = movie.vote_set.filter(vote_type = 'down').count()
        movie.save()
            
        return HttpResponseRedirect('/movie_detail/%s' %pk) 
    else: 
        print 'anonymous user'
        return HttpResponseRedirect('/please_login/')

def vote_show(request, pk, num):
    context = {}
    if request.user.is_authenticated():
        if int(num) == 1:
            vote_type = 'up'
        elif int(num) == 2:
            vote_type = 'down'
        show = Show.objects.get(pk=pk)
        new_vote, created = Vote.objects.get_or_create(user=request.user, show=show)
        new_vote.vote_type = vote_type
        new_vote.save()

        show.upvote_count = show.vote_set.filter(vote_type = 'up').count()
        show.downvote_count = show.vote_set.filter(vote_type = 'down').count()
        show.save()
            
        return HttpResponseRedirect('/show_detail/%s' %pk) 
    else: 
        print 'anonymous user'
        return HttpResponseRedirect('/please_login/')

def vote_episode(request, pk, num):
    context = {}
    if request.user.is_authenticated():
        if int(num) == 1:
            vote_type = 'up'
        elif int(num) == 2:
            vote_type = 'down'
        episode = Episode.objects.get(pk=pk)
        new_vote, created = Vote.objects.get_or_create(user=request.user, episode=episode)
        new_vote.vote_type = vote_type
        new_vote.save()

        episode.upvote_count = episode.vote_set.filter(vote_type = 'up').count()
        episode.downvote_count = episode.vote_set.filter(vote_type = 'down').count()
        episode.save()
            
        return HttpResponseRedirect('/episode_detail/%s' %pk) 
    else: 
        print 'anonymous user'
        return HttpResponseRedirect('/please_login/')

def vote_channel(request, pk, num):
    context = {}
    if request.user.is_authenticated():
        if int(num) == 1:
            vote_type = 'up'
        elif int(num) == 2:
            vote_type = 'down'
        channel = Channel.objects.get(pk=pk)
        new_vote, created = Vote.objects.get_or_create(user=request.user, channel=channel)
        new_vote.vote_type = vote_type
        new_vote.save()

        channel.upvote_count = channel.vote_set.filter(vote_type = 'up').count()
        channel.downvote_count = channel.vote_set.filter(vote_type = 'down').count()
        channel.save()
            
        return HttpResponseRedirect('/channel_detail/%s' %pk) 
    else: 
        print 'anonymous user'
        return HttpResponseRedirect('/please_login/')


        



# def json_response(request):
#     search_string = request.GET.get('search', '')
#     objects = Tracks.objects.filter(track_title__icontains=search_string) 
#     object_list = []
#     for obj in objects:
#         object_list.append({'track_title':obj.track_title, 'track_image_file': obj.track_image_file})

#     return JsonResponse(object_list, safe=False)

# def ajax_search(request):
#     context = {}

#     return render_to_response('ajax_template.html', context, context_instance=RequestContext(request))


