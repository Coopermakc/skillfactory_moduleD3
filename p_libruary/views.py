# from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.template import loader
from p_libruary.models import Book, Publisher, Author, Friend
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from p_libruary.forms import AuthorForm, BookForm, ContactForm, ProfileCretionForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.forms import formset_factory
from django.http.response import HttpResponseRedirect
from django.views.generic.edit import FormView
from allauth.socialaccount.models import SocialAccount
import json

class AuthorCreate(CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('p_libruary:authors_list')
    template_name = 'author_edit.html'

class AuthorList(ListView):
    model = Author
    template_name = 'authors_list.html'


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['full_name', 'birth_year', 'country']
    success_url = reverse_lazy('p_libruary:authors_list')
    template_name = 'author_edit.html'

class AuthorDelete(DeleteView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('p_libruary:authors_list')
    template_name = 'author_delete.html'

class PublisherList(ListView):
    model = Publisher

    def get(self):
        publishers_list = self.model.objects.all()
        return publishers_list

    def put(self, request):
        data = json.loads(request.body)
        publisher = self.model(**data)
        publisher.save()

class PublisherDetailView(DetailView):
    model = Publisher

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)



class RegisterView(FormView):

    form_class = UserCreationForm

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        login(self.request, authenticate(username=username, password=raw_password))
        return super(RegisterView, self).form_valid(form)


class CreateUserProfile(FormView):
    
    form_class = ProfileCretionForm
    template_name = 'profile-create.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('login'))
        return super(CreateUserProfile, self, context).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super(CreateUserProfile, self).form_valid(form)




def books_list(request):
    books = Book.objects.all()
    return HttpResponse(books)


def index(request):
    template = loader.get_template('index.html')
    books = Book.objects.all()
    biblio_data = {
        "title": "Библиотеку",
        "books": books,
    }
    return HttpResponse(template.render(biblio_data, request))

def book_increment(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            book.copy_count += 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')

def book_decrement(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')

def publishers(request):
    template = loader.get_template('publishers.html')
    publishers = Publisher.objects.all()
    publishers_books = {}
    for publisher in publishers:
        publishers_books[publisher.name] = Book.objects.filter(publisher=publisher)
    publishers_data = {
        'publishers_books': publishers_books,
    }
    
    return HttpResponse(template.render(publishers_data, request))

def author_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    if request.method == 'POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        if author_formset.is_valid():
            for author_form in author_formset:
                author_form.save()
            return HttpResponseRedirect(reverse_lazy('author_list'))
    else:
        author_formset = AuthorFormSet(prefix='authors')
    return render(request, 'manage_authors.html', {'author_formset': author_formset})

def books_authors_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    BookFormSet = formset_factory(BookForm, extra=2)
    if request.method =='POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        book_formset = BookFormSet(request.POST, request.FILES, prefix='books')
        if author_formset.is_valid() and book_formset.is_valid():
            for author_form in author_formset:
                author_form.save()
            for book_form in book_formset:
                book_form.save()
            return HttpResponseRedirect(reverse_lazy('author_list'))
    else:
        author_formset = AuthorFormSet(prefix='authors')
        book_formset = BookFormSet(prefix='books')
    return render(
        request,
        'manage_books_authors.html',
        {
            'author_formset': author_formset,
            'book_formset': book_formset,
        }
    )
def friends_list(request):
    template = loader.get_template('friends.html')
    friends = Friend.objects.all()
    data = {
        'friends': friends,
    }
    return HttpResponse(template.render(data, request))