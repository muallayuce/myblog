from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, EditProfileForm, SignUpForm
from .models import Post, Category, Contact
from datetime import datetime
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import TemplateView


def post_list(request):
    posts = Post.objects.all()
    current_year = datetime.now().year
    context = {
        'posts': posts,
        'current_year': current_year,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

def my_view(request):
    categories = Category.objects.all()
    category_counts = []

    for category in categories:
        count = Post.objects.filter(category=category).count()
        category_counts.append((category, count))

    return render(request, 'post_list.html', {'category_counts': category_counts})

def art_category_view(request):
    try:
        art_category = get_object_or_404 (Category, slug='Art') 
        art_posts = Post.objects.filter(category=art_category)
        art_post_count = art_posts.count()  
    except Category.DoesNotExist:
        art_category = None
        art_posts = []
        art_post_count = 0

    return render(request, 'blog/art_category.html', {'art_posts': art_posts, 'art_category': art_category, 'art_post_count': art_post_count})

def sport_category_view(request):
    try:
        sport_category = get_object_or_404 (Category,slug='Sport') 
        sport_posts = Post.objects.filter(category=sport_category)
        sport_post_count = sport_posts.count()  
    except Category.DoesNotExist:
        sport_category = None
        sport_posts = []
        sport_post_count = 0

    return render(request, 'blog/sport_category.html', {'sport_posts':sport_posts, 'sport_category': sport_category, 'sport_post_count': sport_post_count})


def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
          # Handle the form submission here
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        country = request.POST.get('country')
        message = request.POST.get('message')
        
        # Example: Save the data to a database
        contact = Contact(first_name=first_name, last_name=last_name, country=country, message=message)
        contact.save()
        

        # Redirect to a thank you page or any other page
        return redirect('thank_you')

    return render(request, 'contact.html')  

def thank_you(request):
    return render(request, 'thank_you.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')  # Redirect to the post list page
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required  # Ensure the user is logged in
def create_post(request):
    if request.method == 'POST':
        # Handle the form submission
        form = PostForm(request.POST)
        if form.is_valid():
            # Save the new post
            post = form.save(user=request.user, commit=False)
            post.user = request.user  # Assign the current user
            post.save()
            # Redirect to the create_post view (or any other view) after successfully creating a post
            return redirect('post_list')
    else:
        form= PostForm()

    return render(request, 'create_post.html', {'form': form})

@login_required
def delete_post(request, slug):
    # Retrieve the post to delete
    post = get_object_or_404(Post, slug=slug)

    # Check if the logged-in user is the author of the post
    if request.user == post.user:
        # Delete the post
        post.delete()
        # Redirect to a success page or another view (e.g., post list)
        return redirect('post_list')
    else:
        # Return a permission denied response or handle the case where the user is not the author
        return render(request, 'permission_denied.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')  # Redirect to the profile page after successful update
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update the session auth hash
            return redirect('edit_profile')  # Redirect to the user's profile page
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'edit_profile.html', {'form': form})


class GoodbyeView(TemplateView):
    template_name = 'goodbye.html'
