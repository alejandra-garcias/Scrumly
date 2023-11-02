from .models import Task
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render,redirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required




# Create your views here.

class Logueo(LoginView):
    template_name = "Login/login.html"
    field = ['titulo','descripcion','completo']
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('index')
    
class PaginaRegistro(FormView):
    template_name = "Login/registro.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')

    def form_valid(self,form):
        usuario = form.save()
        if usuario is not None:
            login(self.request,usuario)
        return super(PaginaRegistro,self).form_valid(form)
    
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super(PaginaRegistro,self).get(*args,**kwargs)

@login_required
def index(request):
    user_tasks = Task.objects.filter(user=request.user)
    db_data = Task.objects.all()
    context = {
        "db_data": user_tasks[::-1],
        "update": None
    }
    return render(request, "TaskManager/index.html", context)

@login_required
def insert(request):
    try:
        task_subject = request.POST["subject"]
        task_description = request.POST["description"]
        task_priority = request.POST.get("priority")
        task_completed = request.POST.get("completed")

        if task_priority == "on":
            task_priority = True
        else:
            task_priority = False
        
        if task_completed == "on":
            task_completed = True
        else:
            task_completed = False

        if task_subject == "":
            raise ValueError("El texto no puede estar en vacio.")
        db_data = Task(user=request.user,subject=task_subject, description=task_description,completed=task_completed,priority=task_priority)
        db_data.save()
        return HttpResponseRedirect(reverse("index")) 
    except ValueError as err:
        print(err)
        return HttpResponseRedirect(reverse("index")) 

@login_required
def update(request):
    task_id = request.POST["id"]
    task_subject = request.POST["subject"]
    task_description = request.POST["description"]
    task_priority = request.POST.get("priority") == "true"  # Convierte la cadena "true" en True, de lo contrario, False
    task_completed = request.POST.get("completed") == "true"  # Convierte la cadena "true" en True, de lo contrario, False

    print(task_completed)
    print(task_priority)

    db_data = Task.objects.get(pk=task_id)
    db_data.subject = task_subject
    db_data.description = task_description
    db_data.priority = task_priority
    db_data.completed = task_completed
    db_data.save()

    return HttpResponseRedirect(reverse("index"))


@login_required
def update_form(request, task_id):
    user_tasks = Task.objects.filter(user=request.user)
    db_data_only = Task.objects.get(pk=task_id)
    print(db_data_only)
    context = {
        "db_data": user_tasks[::-1],
        "update": db_data_only
    }
    return render(request, "TaskManager/index.html", context)

@login_required
def delete(request, task_id):
    db_data = Task.objects.filter(id=task_id)
    db_data.delete()
    return HttpResponseRedirect(reverse("index")) 

def search(request):
    query = request.GET.get('query', '')  # Obtener el término de búsqueda de la URL
    user_tasks = Task.objects.filter(user=request.user, subject__icontains=query)
    
    context = {
        "db_data": user_tasks[::-1],
        "update": None
    }
    return render(request, "TaskManager/index.html", context)

from django.shortcuts import render
from django.http import JsonResponse
import openai
from .models import Chatbot
from django.utils import timezone

openai_api_key = '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'
openai.api_key = openai_api_key
def ask_openai(message):
    response= openai.ChatCompletion.create(
        model = "gpt-3.5-turbo", #text-davinci-003
        messages=[
            {'role':"system", "content":"You are a helpful assistant"},
            {"role":"user","content":message},
        ]
    )

    answer = response.choices[0].message.content.strip()
    return answer

def chatbot(request,):
    chats = Chatbot.objects.filter(user=request.user)
    if request.method == 'POST':
        message =  request.POST.get('message')
        response = ask_openai(message)
        chat= Chatbot(user=request.user , message= message , response= response, created_at= timezone.now)
        chat.save()
        return JsonResponse({'message':message, 'response':response})
    return render(request, '/TaskManager/index.html',{'chats':chats})
