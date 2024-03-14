from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FileEntry
from .forms import FileEntryForm
from django.http import HttpResponse, Http404,FileResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout



def home_view(request):
    return render(request, 'main/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') 
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

@login_required(login_url='/')  
def logout_view(request):
    logout(request)
    return redirect('login') 

@login_required(login_url='/')  
def upload_file(request):
    if request.method == 'POST':
        form = FileEntryForm(request.POST, request.FILES)
        if form.is_valid():
            file_entry = form.save(commit=False)
            file_entry.user = request.user
            file_entry.save()
            return redirect('file_list')
    else:
        form = FileEntryForm()
    return render(request, 'main/upload_file.html', {'form': form})

@login_required(login_url='/')  
def file_list(request):
    if request.method == 'POST':
        form = FileEntryForm(request.POST, request.FILES)
        if form.is_valid():
            file_entry = form.save(commit=False)
            file_entry.user = request.user  
            file_entry.save()
            return redirect('file_list')
    else:
        form = FileEntryForm()
    
    files = FileEntry.objects.filter(user=request.user)  # Display only user's files
    return render(request, 'main/file_list.html', {'files': files, 'form': form})


@login_required(login_url='/')
def update_file_entry(request, file_id):
    file_entry = get_object_or_404(FileEntry, id=file_id, user=request.user)
    if file_entry:
        if request.method == "POST":
            form = FileEntryForm(request.POST, request.FILES, instance=file_entry)
            if form.is_valid():
                form.save()
                return redirect('file_list')
        else:
            form = FileEntryForm(instance=file_entry)
        return render(request, 'main/edit_file_entry.html', {'form': form})
    else:
        return redirect('home')


@login_required(login_url='/')
def delete_file_entry(request, file_id):
    file_entry = get_object_or_404(FileEntry, id=file_id, user=request.user)
    if request.method == 'POST':
        file_entry.delete()
        return redirect('file_list')
    return redirect('home')  



@login_required(login_url='/')  
def download_file(request, file_id):
    try:
        file_entry = FileEntry.objects.get(id=file_id)
        if file_entry.user != request.user:
            raise Http404("You are not authorized to download this file.")

        file_entry = FileEntry.objects.get(id=file_id, user=request.user)  
        response = FileResponse(file_entry.file.open(), as_attachment=True, filename=file_entry.file.name)
        return response
    except FileEntry.DoesNotExist:
        raise Http404("File does not exist")