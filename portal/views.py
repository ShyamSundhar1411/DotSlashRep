from django.shortcuts import render,get_object_or_404,redirect
from django.views import generic
from django.utils import timezone
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import Http404,HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ToDo,Note
# Create your views here.
#Class Based Views
class ToDoCreateView(LoginRequiredMixin,generic.CreateView):
    model = ToDo
    fields = ['title','memo','isImportant']
    template_name = "portal/todos/CreateToDo.html"
    success_url = reverse_lazy("view_all_todos")
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(ToDoCreateView, self).form_valid(form)
class ToDoUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = ToDo
    slug_field = ToDo.slug
    fields = ['title','memo','isImportant','isCompleted']
    template_name = "portal/todos/UpdateToDo.html"
    success_url = reverse_lazy('view_all_todos')
    def get_object(self):
        todo = super(ToDoUpdateView, self).get_object()
        if todo.user != self.request.user:
            raise Http404
        return todo
#Notes
class NoteCreateView(LoginRequiredMixin,generic.CreateView):
    model  = Note
    fields = ['title','subject','notes','important']
    template_name = "portal/notes/CreateNote.html"
    success_url = reverse_lazy("view_all_notes")
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(NoteCreateView,self).form_valid(form)
class NoteDetailView(LoginRequiredMixin,generic.DetailView):
    model = Note
    slug_field = Note.slug
    template_name = "portal/notes/NoteDetail.html"
class NoteUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = Note
    slug_field = Note.slug
    fields = ['title','subject','notes','important']
    template_name = "portal/notes/UpdateNote.html"
    def get_object(self):
        note = super(NoteUpdateView,self).get_object()
        if note.user != self.request.user:
            raise Http404
        return note
    def get_success_url(self):
        pk = self.kwargs["pk"]
        slug = self.kwargs["slug"]
        messages.success(self.request,'Updated Successfully')
        return reverse("view_detailed_note", kwargs={"slug":slug,"pk": pk})
class NoteDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = Note
    slug_field = Note.slug
    template_name = "portal/notes/DeleteNote.html"
    def get_object(self):
        note = super(NoteDeleteView,self).get_object()
        if note.user != self.request.user:
            raise Http404
        return note
    def get_success_url(self):
        note = super(NoteDeleteView,self).get_object()
        return reverse('view_all_notes')
#Function Based Views
def home(request):
    return render(request,'portal/home.html')
def portal(request):
    return render(request,'portal/portal.html')
@login_required
def todos(request):
    todos = ToDo.objects.filter(user = request.user)
    count = ToDo.objects.filter(user = request.user,isCompleted = False).count()
    search_input = request.GET.get('search') or ''
    if search_input:
        todos = ToDo.objects.filter(user = request.user,title__contains = search_input)
    return render(request,'portal/todos/viewtodos.html',{'todos':todos,'count':count,'search_input':search_input})
@login_required
def deletetodo(request,pk,slug):
    todo = get_object_or_404(ToDo,user = request.user,id = pk, slug = slug)
    if request.method == "POST":
        todo.delete()
        messages.success(request,"ToDo Deleted Sucessfully")
        return redirect('view_all_todos')
#Notes
def notes(request):
    note = Note.objects.filter(user = request.user).order_by('-updated_on')
    page = request.GET.get('page', 1)
    paginator = Paginator(note,3)
    note_count = paginator.count
    search_input = request.GET.get('search') or ''
    try:
        notes = paginator.page(page)
    except PageNotAnInteger :
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)
    if search_input:
        notes = Note.objects.filter(user = request.user,title__contains = search_input)
    return render(request,'portal/notes/viewnotes.html',{"Notes":notes,'note_count':note_count,'input':search_input})
    