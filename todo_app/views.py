# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm
from .models import Task
from django.contrib.auth.decorators import login_required
from .forms import TaskForm

def home(request):
    return render(request, 'todo_app/index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserRegistrationForm()
    return render(request, 'todo_app/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'todo_app/login.html'

@login_required
def todo_list(request):
    tasks = Task.objects.filter(user=request.user)
    rooms = Room.objects.all()
    return render(request, 'todo_app/todo_list.html', {'tasks': tasks,'rooms': rooms})

# todo_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TaskForm, OpenAIForm
from .utils import generate_openai_response
@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('todo_list')
    else:
        form = TaskForm()
    return render(request, 'todo_app/add_task.html', {'form': form})


@login_required
def generate_openai_response_view(request):
    if request.method == 'POST':
        openai_form = OpenAIForm(request.POST)
        if openai_form.is_valid():
            prompt = openai_form.cleaned_data['prompt']
            openai_response = generate_openai_response(prompt)
            return render(request, 'todo_app/openai_response.html', {'openai_response': openai_response})

    return redirect('add_task')

@login_required
def edit_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo_app/edit_task.html', {'form': form, 'task': task})

@login_required
def delete_task(request, task_id):
    task = Task.objects.get(pk=task_id,)
    if request.method == 'POST':
        task.delete()
        return redirect('todo_list')
    return render(request, 'todo_app/delete_task.html', {'task': task})


@login_required
def all_user_tasks(request):
    if request.user.is_superuser:
        tasks = Task.objects.all()
        return render(request, 'todo_app/all_user_tasks.html', {'tasks': tasks})
    else:
        return redirect('todo_list')
@login_required
def mark_task_completed(request, task_id):
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        task.completed = not task.completed
        task.save()
    return redirect('todo_list')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task

@login_required
@login_required
def sleep_recommendation(request):
    if request.method == "POST":
        sleep_hours = int(request.POST.get("sleepHours"))
        work_hours = int(request.POST.get("workHours"))

        recommendation = ""
        work_recommendation = ""

        if sleep_hours >= 7 and work_hours <= 8:
            recommendation = "Great job! You're getting enough sleep and maintaining a balanced work schedule."
        elif sleep_hours < 7:
            recommendation = "Consider getting more sleep to stay refreshed and focused."
        elif work_hours > 8:
            recommendation = "You might want to consider taking short breaks or naps to prevent burnout."
        if work_hours < 5:
                work_recommendation = "Your work hours are quite low. Make sure to maintain a balanced work routine."
        elif work_hours > 10:
                work_recommendation = "Your work hours are high. Remember to take regular breaks and get enough rest."

        return render(request, "sleep.html", {"user_recommendation": recommendation, "work_recommendation": work_recommendation})

    return render(request, "sleep.html")


    # rooms/views.py
# rooms/views.py
from django.shortcuts import render, redirect
from .forms import RoomForm
from .models import Room

def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            return redirect('room_detail', room_id=room.id)
    else:
        form = RoomForm()

    return render(request, 'todo_app/create_room.html', {'form': form})
def inpp(request):
    tasks = Task.objects.filter(user=request.user)
    rooms = Room.objects.all()
    return render(request, 'todo_app/rooms.html', {'tasks': tasks,'rooms': rooms})
def room_detail(request, room_id):
    room = Room.objects.get(id=room_id)
    return render(request, 'todo_app/room_detail.html', {'room': room})

def connect_to_room(request):
    error_message = None  # Initialize error_message
    if request.method == 'POST':
        room_name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            room = Room.objects.get(name=room_name, password=password)
            return redirect('room_detail', room_id=room.id)
        except Room.DoesNotExist:
            error_message = 'Invalid room name or password.'

    return render(request, 'todo_app/connect_to_room.html', {'error_message': error_message})



# todo_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Room

def room_detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    rooms = Room.objects.all()
    tasks = Task.objects.all()

    if request.method == 'POST':
        entered_password = request.POST.get('password', '')
        if room.is_password_valid(entered_password):
            return render(request, 'todo_app/todo_list.html', {'room': room,'tasks':tasks})
        else:
            error_message = 'Invalid password. Please try again.'
            return render(request, 'todo_app/password_prompt.html', {'error_message': error_message})

    return render(request, 'todo_app/password_prompt.html', {'room': room})
