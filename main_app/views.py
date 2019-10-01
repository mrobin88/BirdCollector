from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FeedingForm
import uuid
import boto3
from .models import Bird, Toy, Photo

S3_BASE_URL = 'https://s3.us-west-1.amazonaws.com/'
BUCKET = 'buckets-mlr'


class BirdCreate(LoginRequiredMixin,CreateView):
  model = Bird
  fields = ['name', 'breed', 'description', 'age' ]
  def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BirdUpdate(LoginRequiredMixin,UpdateView):
  model = Bird
  fields = ['breed', 'description', 'age']

class BirdDelete(LoginRequiredMixin,DeleteView):
  model = Bird
  success_url = '/birds/'
  
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def birds_index(request):
  birds = Bird.objects.filter(user=request.user)
  return render(request, 'birds/index.html', { 'birds': birds })
@login_required
def birds_detail(request, bird_id):
  bird = Bird.objects.get(id=bird_id)

  toys_bird_doesnt_have = Toy.objects.exclude(id__in = bird.toys.all().values_list('id')) 
  feeding_form = FeedingForm()
  return render(request, 'birds/detail.html', {
    'bird': bird, 'feeding_form': feeding_form,
  
    'toys': toys_bird_doesnt_have
  })
@login_required
def assoc_toy(request, bird_id, toy_id):

  Bird.objects.get(id=bird_id).toys.add(toy_id)
  return redirect('detail', bird_id=bird_id)

@login_required
def add_feeding(request, bird_id):
	# create the ModelForm using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
  
    new_feeding = form.save(commit=False)
    new_feeding.bird_id = bird_id
    new_feeding.save()
  return redirect('detail', bird_id=bird_id)

def add_photo(request, bird_id):
  
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
      
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
          
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
          
            photo = Photo(url=url, bird_id=bird_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
            
    return redirect('detail', bird_id=bird_id)

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'

def signup(request):
  error_message = ''
  if request.method == 'POST':
  
  
    form = UserCreationForm(request.POST)
    if form.is_valid():
    
      user = form.save()
    
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'

  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

