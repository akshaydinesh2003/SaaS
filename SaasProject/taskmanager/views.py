from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, UserProfile, RoleRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .forms import TaskForm, RoleRequestForm
from django.contrib.auth.models import User

@login_required
def dashboard(request):
    # Current tasks: tasks that are in progress
    current_tasks = Task.objects.filter(status='In Progress', assigned_to=request.user)

    # Finished tasks: tasks that are completed
    finished_tasks = Task.objects.filter(status='Completed', assigned_to=request.user)

    # Upcoming tasks: tasks that are pending and the due date is in the future
    upcoming_tasks = Task.objects.filter(status='Pending', due_date__gt=timezone.now(), assigned_to=request.user)

    context = {
        'current_tasks': current_tasks,
        'finished_tasks': finished_tasks,
        'upcoming_tasks': upcoming_tasks,
    }

    return render(request, 'dashboard.html', context)

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created successfully.')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})

@login_required
def assign_task(request):
    if request.user.userprofile.role in ['admin', 'manager']:
        if request.method == 'POST':
            task_id = request.POST.get('task_id')
            user_id = request.POST.get('user_id')
            task = get_object_or_404(Task, id=task_id)
            user = get_object_or_404(User, id=user_id)
            task.assigned_to = user
            task.save()
            messages.success(request, 'Task assigned successfully.')
            return redirect('dashboard')
        tasks = Task.objects.filter(assigned_to=None)
        users = User.objects.all()
        return render(request, 'assign_task.html', {'tasks': tasks, 'users': users})
    else:
        messages.error(request, 'You are not authorized to assign tasks.')
        return redirect('dashboard')

@login_required
def request_role_change(request):
    if request.method == 'POST':
        form = RoleRequestForm(request.POST)
        if form.is_valid():
            role_request = form.save(commit=False)
            role_request.user = request.user
            role_request.save()
            messages.success(request, 'Role change request submitted successfully.')
            return redirect('dashboard')
    else:
        form = RoleRequestForm()
    return render(request, 'request_role_change.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
@login_required
def manage_role_requests(request):
    # Fetch all pending role requests
    role_requests = RoleRequest.objects.filter(status='Pending')
    return render(request, 'manage_role_requests.html', {'role_requests': role_requests})

@user_passes_test(lambda u: u.is_superuser)
@login_required
def process_role_request(request, role_request_id):
    role_request = get_object_or_404(RoleRequest, id=role_request_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            role_request.status = 'Approved'
            role_request.user.userprofile.role = role_request.requested_role
            role_request.user.userprofile.save()
            messages.success(request, 'Role request approved successfully.')
        elif action == 'deny':
            role_request.status = 'Denied'
            messages.info(request, 'Role request denied.')

        role_request.save()
        return redirect('manage_role_requests')

    return render(request, 'process_role_request.html', {'role_request': role_request})
