from django.shortcuts import render, redirect, get_object_or_404
from .models import VisualStory, StoryCard, Category, VideoNews, SubCategory, NewsArticle, VideoAds, ImageAds, Profile, Comment
from django.http import JsonResponse
from django.utils import timezone
import random
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Q
from django.core.paginator import Paginator

def admin_check(user):
    return user.is_authenticated and user.is_superuser 

# 3. Check if user is a regular user (neither staff nor superuser)
def regular_user_check(user):
    return user.is_authenticated and not user.is_superuser

def check_username(request):
    """AJAX view to check if a username already exists."""
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

def check_email(request):
    """AJAX view to check if an email is already in use."""
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        phone = request.POST['phone']
        address = request.POST['address']

        category1 = request.POST.get('category1')
        category2 = request.POST.get('category2')
        category3 = request.POST.get('category3')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken.')
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password, email=email,
                                        first_name=first_name, last_name=last_name)
        user.save()

        # Save the additional information to the Profile model
        category1_instance = Category.objects.get(id=category1)
        category2_instance = Category.objects.get(id=category2)
        category3_instance = Category.objects.get(id=category3)

        profile = Profile.objects.create(
            user=user,
            phone=phone,
            address=address,
            category1=category1_instance,
            category2=category2_instance,
            category3=category3_instance
        )
        profile.save()

        auth_login(request, user)  # Log the user in after signup
        return redirect('login')

    categories = Category.objects.all()  # Load categories for dropdowns
    return render(request, 'signup.html', {'categories': categories})

from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import redirect, render

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            
            # Check if the user is a superuser and redirect accordingly
            if user.is_superuser:
                return redirect('admin_dashboard')  # Redirect to admin dashboard
            else:
                return redirect('front_page')  # Redirect to home page for normal users
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    
    return render(request, 'login.html')



@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


def lgout(request):
    auth.logout(request)
    return redirect ('front_page')


# Create your views here.
@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def manage_categorys(request):
    categorys = Category.objects.all()
    # return redirect('manage_categorys')
    

    context = {
        'categorys': categorys
    }
    
    return render(request, 'manage_categorys.html', context)


@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if category_name:
            Category.objects.create(name=category_name)
            return redirect('manage_categorys')

    categorys = Category.objects.all()
    return render(request, 'manage_categorys.html', {'categorys': categorys})

@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def delete_category(request, category_id):
    # Get the category to be deleted
    category = get_object_or_404(Category, id=category_id)
    
    
    # Delete the category itself
    category.delete()
    
    # Retrieve the updated list of categorys and notification count
    categorys = Category.objects.all()
    
    
    # Redirect to the admin dashboard
    return render(request, 'manage_categorys.html', {'categorys': categorys})

@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def add_visual_story(request):
    categories = Category.objects.all()  # To populate the category dropdown

    if request.method == 'POST':
        # Get data from POST request
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        location = request.POST.get('location')  # Capture location input
        
        # Save VisualStory
        visual_story = VisualStory.objects.create(title=title, description=description, category=category, location=location)
        
        # Handle dynamic story cards (handling multiple inputs for each story card)
        card_index = 1
        while True:
            image = request.FILES.get(f'card_image_{card_index}')
            heading = request.POST.get(f'card_heading_{card_index}')
            short_text = request.POST.get(f'card_short_text_{card_index}')

            if not (image and heading and short_text):
                break

            # Save each StoryCard
            StoryCard.objects.create(visual_story=visual_story, image=image, heading=heading, short_text=short_text)
            card_index += 1

        messages.success(request, 'Visual story added successfully!')

        return redirect('admin_dashboard')  # Redirect after saving

    return render(request, 'add_visual_story.html', {'categories': categories})

@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def visual_story_list(request):
    stories = VisualStory.objects.all()
    return render(request, 'visual_story_list.html', {'stories': stories})

# Edit View
@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def edit_visual_story(request, story_id):
    story = get_object_or_404(VisualStory, id=story_id)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        # Update the VisualStory details
        story.title = request.POST.get('title')
        story.description = request.POST.get('description')
        category_id = request.POST.get('category')
        story.category = get_object_or_404(Category, id=category_id)
        story.location = request.POST.get('location') or None  # Handle empty input
        story.save()

        # Update existing StoryCards
        for card in story.story_cards.all():
            card.heading = request.POST.get(f'card_heading_{card.id}')
            card.short_text = request.POST.get(f'card_short_text_{card.id}')
            if request.FILES.get(f'card_image_{card.id}'):
                card.image = request.FILES.get(f'card_image_{card.id}')
            card.save()

        return redirect('visual_story_list')

    return render(request, 'edit_visual_story.html', {
        'story': story, 
        'categories': categories
    })

# Delete View
@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def delete_visual_story(request, story_id):
    story = get_object_or_404(VisualStory, id=story_id)
    story.delete()
    return redirect('visual_story_list')

@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def add_video_news(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        video = request.FILES.get('video')
        location = request.POST.get('location')  # Capture location input

        # Fetch the selected category
        category = Category.objects.get(id=category_id)

        # Create a new VideoNews object and save it
        video_news = VideoNews(title=title, description=description, category=category, video=video, location=location)
        video_news.save()

        messages.success(request, 'Video added successfully!')
        return redirect('admin_dashboard')  # Redirect to a page that lists all VideoNews entries

    return render(request, 'add_video_news.html', {'categories': categories})

@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def video_news_list(request):
    video_news = VideoNews.objects.all()
    return render(request, 'video_news_list.html', {'video_news': video_news})

@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def delete_video_news(request, video_id):
    video_news = get_object_or_404(VideoNews, id=video_id)
    video_news.delete()
    return redirect('video_news_list')

@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def edit_video_news(request, video_id):
    video_news = get_object_or_404(VideoNews, id=video_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        video = request.FILES.get('video', None)
        location = request.POST.get('location')

        

        category = Category.objects.get(id=category_id)
        video_news.title = title
        video_news.description = description
        video_news.category = category
        video_news.location = location

        # Only update the video if a new file is uploaded
        if video:
            video_news.video = video

        video_news.save()
        return redirect('video_news_list')

    return render(request, 'edit_video_news.html', {
        'video_news': video_news,
        'categories': categories,
    })

@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def subcategory_view(request):
    subcategories = SubCategory.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        # Add new subcategory
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        if name and category_id:
            category = Category.objects.get(id=category_id)
            SubCategory.objects.create(name=name, category=category)
        return redirect('subcategory-list')

    return render(request, 'subcategory_list.html', {
        'subcategories': subcategories,
        'categories': categories
    })

@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def delete_subcategory(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)
    subcategory.delete()
    return redirect('subcategory-list')



@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def add_news_article(request):
    selected_category_id = None
    subcategories = SubCategory.objects.none()

    if request.method == 'POST':
        # Capture the selected category from the form submission
        selected_category_id = request.POST.get('category')
        if selected_category_id:
            subcategories = SubCategory.objects.filter(category_id=selected_category_id)

        # Check if we are saving the article
        if 'save_changes' in request.POST:  # Ensure this matches your form button name
            title = request.POST.get('title')
            content = request.POST.get('content')
            reporter = request.POST.get('reporter')
            subcategory_id = request.POST.get('subcategory')
            published_date = request.POST.get('published_date')
            location = request.POST.get('location')  # Capture location input
            image = request.FILES.get('image')  # Handle the image file here

            # Ensure subcategory is selected
            if subcategory_id:
                try:
                    # Create the news article
                    NewsArticle.objects.create(
                        title=title,
                        content=content,
                        reporter=reporter,
                        subcategory_id=subcategory_id,
                        published_date=published_date,
                        location = location,
                        image=image  # Save the image if provided
                    )
                    messages.success(request, 'News article added successfully!')
                    return redirect('admin_dashboard')  # Adjust the redirect as needed
                except Exception as e:
                    messages.error(request, f"Error creating article: {e}")
                    return redirect('admin_dashboard')  # Adjust the redirect as needed

    # Load all categories for the dropdown
    categories = Category.objects.all()

    return render(request, 'add_news_article.html', {
        'categories': categories,
        'subcategories': subcategories,
        'selected_category': int(selected_category_id) if selected_category_id else None
    })


@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def list_news_articles(request):
    articles = NewsArticle.objects.all()

    # Set up pagination, 12 articles per page
    paginator = Paginator(articles, 12)  # Show 12 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass the paginated articles to the template
    return render(request, 'list_news_articles.html', {'page_obj': page_obj})

# Delete a News Article
@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def delete_news_article(request, article_id):
    news = get_object_or_404(NewsArticle, id=article_id)
    news.delete()
    return redirect('list_news_articles')



# Edit a News Article
@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def edit_news_article(request, article_id):
    article = get_object_or_404(NewsArticle, id=article_id)

    # Check if the category is being selected after form submission
    if request.method == 'POST':
        selected_category_id = request.POST.get('category')
        subcategories = SubCategory.objects.filter(category_id=selected_category_id)
    else:
        selected_category_id = article.subcategory.category.id
        subcategories = SubCategory.objects.filter(category_id=selected_category_id)

    if request.method == 'POST' and 'save_changes' in request.POST:
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.reporter = request.POST.get('reporter')
        article.subcategory_id = request.POST.get('subcategory')
        article.published_date = request.POST.get('published_date') or article.published_date

        # Handle the location
        article.location = request.POST.get('location') or None  # Handle empty input

        # Handle the image
        if 'image' in request.FILES:
            article.image = request.FILES['image']  # Update image if a new one is uploaded

        article.save()
        return redirect('list_news_articles')

    categories = Category.objects.all()

    return render(request, 'edit_news_article.html', {
        'article': article,
        'categories': categories,
        'subcategories': subcategories,
        'selected_category': int(selected_category_id),  # Pass the selected category ID
        'selected_subcategory': article.subcategory.id
    })

@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def add_video_ad(request):
    if request.method == 'POST':
        company = request.POST.get('company')
        description = request.POST.get('description')
        video = request.FILES.get('video')

        VideoAds.objects.create(
            company=company,
            description=description,
            video=video
        )
        messages.success(request, 'Video ad added successfully!')
        return redirect('admin_dashboard')  # Redirect to a page that lists the video ads

    return render(request, 'add_video_ad.html')

@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def list_video_ads(request):
    video_ads = VideoAds.objects.all()
    return render(request, 'list_video_ads.html', {'video_ads': video_ads})

@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def edit_video_ad(request, ad_id):
    video_ad = get_object_or_404(VideoAds, id=ad_id)
    
    if request.method == 'POST':
        video_ad.company = request.POST.get('company')
        video_ad.description = request.POST.get('description')
        if request.FILES.get('video'):
            video_ad.video = request.FILES.get('video')
        video_ad.save()
        return redirect('list_video_ads')

    return render(request, 'edit_video_ad.html', {'video_ad': video_ad})

@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def delete_video_ad(request, ad_id):
    if request.method == 'POST' or request.method == 'GET':  # Handle POST or GET request
        ad = get_object_or_404(VideoAds, id=ad_id)
        ad.delete()
        return redirect('list_video_ads')
    
@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def add_image_ad(request):
    if request.method == 'POST':
        company = request.POST.get('company')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        link = request.POST.get('link')  # Get the link from the form

        # Save the uploaded image file
        if image:
            fs = FileSystemStorage()
            image_name = fs.save(image.name, image)

        ImageAds.objects.create(
            company=company,
            description=description,
            image=image,
            link=link  # Save the link
        )
        messages.success(request, 'Image ad added successfully!')
        return redirect('admin_dashboard')

    return render(request, 'add_image_ad.html')

@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def list_image_ads(request):
    ads = ImageAds.objects.all()

    if request.method == 'POST' and 'delete_ad_id' in request.POST:
        ad_id = request.POST.get('delete_ad_id')
        ad = get_object_or_404(ImageAds, id=ad_id)
        ad.delete()
        return redirect('list_image_ads')

    return render(request, 'list_image_ads.html', {'ads': ads})

# View to edit an existing image ad
@login_required(login_url='login')
@user_passes_test(admin_check, login_url='login') 
def edit_image_ad(request, ad_id):
    ad = get_object_or_404(ImageAds, id=ad_id)
    
    if request.method == 'POST':
        ad.company = request.POST.get('company')
        ad.description = request.POST.get('description')
        ad.link = request.POST.get('link')  # Get the new link value
        
        # Check if a new image was uploaded
        if 'image' in request.FILES:
            ad.image = request.FILES['image']

        ad.save()
        return redirect('list_image_ads')

    return render(request, 'edit_image_ad.html', {'ad': ad})


def front_page(request):
    all_articles = NewsArticle.objects.all()
    
    # Select one main article (the latest one)
    main_article = all_articles.order_by('-id').first()

    all_articles = NewsArticle.objects.all().order_by('-id')

    
    # Select a random set of smaller articles (excluding the main one)
    random_articles = all_articles.exclude(id=main_article.id)[:4]
    articles = NewsArticle.objects.all().order_by('-id')[5:9]
  # Randomly select 4 articles
    football_articles = NewsArticle.objects.filter(subcategory__name="Football")[:6]  # Football-specific news
    ads = ImageAds.objects.all()  # Fetch all advertisement images
    trending_articles = NewsArticle.objects.all().order_by('-id')[:12]
    video_news = VideoNews.objects.all().order_by('-id')
    video_ads = VideoAds.objects.all().order_by('-id')
    visual_stories = VisualStory.objects.all().order_by('-id')  # Latest first
    

    context = {
        'articles': articles,
        'football_articles': football_articles,
        'ads': ads,
        'trending_articles': trending_articles,
        'video_news': video_news,
        'video_ads': video_ads,
        'visual_stories': visual_stories,
        'main_article': main_article,
        'random_articles': random_articles,
       
    }

    return render(request, 'front_page.html', context)

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import NewsArticle, Comment, ImageAds, VideoAds
from django.utils import timezone


def news_detail(request, article_id):
    # Fetch the article by its ID
    article = get_object_or_404(NewsArticle, id=article_id)
    comments = Comment.objects.filter(article=article).order_by('-created_at')
    ads = ImageAds.objects.all()  # Fetch all advertisement images
    video_ads = VideoAds.objects.all().order_by('-id')
    latest_news = NewsArticle.objects.exclude(id=article_id).order_by('-id')[:10]
    aanews_articles = NewsArticle.objects.exclude(id=article_id).order_by('-id')[:10]
    saved = article in request.user.profile.saved_articles.all() if request.user.is_authenticated else False

    # Extract the country, state, and city from the location (splitting by dash)
    if article.location:
        location_parts = article.location.split('-')
        country = location_parts[0] if len(location_parts) > 0 else None
        state = location_parts[1] if len(location_parts) > 1 else None
        city = location_parts[2] if len(location_parts) > 2 else None
    else:
        country = state = city = None

    


    if request.method == 'POST':
        # Handle comment creation, editing, or deletion
        content = request.POST.get('content')
        comment_id = request.POST.get('comment_id')
        action = request.POST.get('action')

        if action == 'delete':
            # Handle comment deletion
            comment = get_object_or_404(Comment, id=comment_id, user=request.user)
            comment.delete()
            return redirect('news_detail', article_id=article_id)

        elif comment_id:
            # Handle comment editing
            comment = get_object_or_404(Comment, id=comment_id, user=request.user)
            if content:
                comment.content = content
                comment.save()
                return redirect('news_detail', article_id=article_id)
        else:
            # Handle new comment creation
            if content:
                Comment.objects.create(
                    article=article,
                    user=request.user,
                    content=content,
                    created_at=timezone.now()
                )
                return redirect('news_detail', article_id=article_id)

    return render(request, 'news_detail.html', {
        'article': article,
        'comments': comments,
        'ads': ads,
        'video_ads': video_ads,
        'country': country,
        'state': state,
        'city': city,
        'latest_news' : latest_news,
        'aanews_articles' : aanews_articles,
        'saved' : saved
    })


def video_detail(request, video_id):
    video = get_object_or_404(VideoNews, id=video_id)
    ads = ImageAds.objects.all()  # Fetch all advertisement images
    video_ads = VideoAds.objects.all().order_by('-id')
    latest_news = NewsArticle.objects.order_by('-id')[:10]
    aavideo_news_list = VideoNews.objects.exclude(id=video_id).order_by('-id')[:10]
    saved = video in request.user.profile.saved_videos.all() if request.user.is_authenticated else False

    # Extract the country, state, and city from the location (splitting by dash)
    if video.location:
        location_parts = video.location.split('-')
        country = location_parts[0] if len(location_parts) > 0 else None
        state = location_parts[1] if len(location_parts) > 1 else None
        city = location_parts[2] if len(location_parts) > 2 else None
    else:
        country = state = city = None

    return render(request, 'video_detail.html', {
        'video': video,
        'ads': ads,
        'video_ads': video_ads,
        'country': country,
        'state': state,
        'city': city,
        'latest_news': latest_news,
        'aavideo_news_list' : aavideo_news_list,
        'saved' : saved
    })



def story_card_detail(request, visual_story_id):
    visual_story = get_object_or_404(VisualStory, id=visual_story_id)
    story_cards = StoryCard.objects.filter(visual_story=visual_story)
    ads = ImageAds.objects.all()  # Fetch all advertisement images
    video_ads = VideoAds.objects.all().order_by('-id')
    latest_news = NewsArticle.objects.order_by('-id')[:10]
    aavisual_stories = VisualStory.objects.exclude(id=visual_story_id).order_by('-id')[:10]
    context = {
        'visual_story': visual_story,
        'story_cards': story_cards,
        'ads': ads,
        'video_ads': video_ads,
        'latest_news': latest_news,
        'aavisual_stories': aavisual_stories,
    }
    return render(request, 'story_card_detail.html', context)


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    # Fetch VideoNews and VisualStory entries matching the category
    video_news = VideoNews.objects.filter(category=category).order_by('-published_date')[:4]
    visual_stories = VisualStory.objects.filter(category=category).order_by('-published_date')[:4]
    # Get all subcategories under the selected category
    subcategories = SubCategory.objects.filter(category=category)
    ads = ImageAds.objects.all()  # Fetch all advertisement images
    video_ads = VideoAds.objects.all().order_by('-id')
    
    # Get all NewsArticle entries where the subcategory is in the selected subcategories
    articles = NewsArticle.objects.filter(subcategory__in=subcategories)
    
    context = {
        'category': category,
        'video_news': video_news,
        'visual_stories': visual_stories,
        'articles': articles,
        'ads': ads,
        'video_ads': video_ads
    }
    return render(request, 'category_detail.html', context)


def news_by_category(request):
    selected_category = request.GET.get('category')  # Get the selected category from query params
    categories = Category.objects.all()  # Fetch all categories for the dropdown
    news_by_subcategory = {}
    ads = ImageAds.objects.all()  # Fetch all advertisement images
    video_ads = VideoAds.objects.all().order_by('-id')

    if selected_category:
        category = get_object_or_404(Category, id=selected_category)
        subcategories = SubCategory.objects.filter(category=category)
        
        for subcategory in subcategories:
            news_by_subcategory[subcategory] = NewsArticle.objects.filter(subcategory=subcategory)
    
    context = {
        'categories': categories,
        'news_by_subcategory': news_by_subcategory,
        'selected_category': selected_category,
        'ads': ads,
        'video_ads': video_ads
    }

    return render(request, 'news_by_category.html', context)


def video_and_visual_stories(request):
    categories = Category.objects.all()  # Get all categories for the dropdown
    selected_category = request.GET.get('category', None)  # Get the selected category from the dropdown
    video_news = []
    visual_stories = []
    ads = ImageAds.objects.all()  # Fetch all advertisement images
    video_ads = VideoAds.objects.all().order_by('-id')

    if selected_category:
        selected_category_obj = get_object_or_404(Category, id=selected_category)

        # Filter VideoNews and VisualStory by the selected category
        video_news = VideoNews.objects.filter(category=selected_category_obj)
        visual_stories = VisualStory.objects.filter(category=selected_category_obj)

    context = {
        'categories': categories,
        'selected_category': selected_category,
        'video_news': video_news,
        'visual_stories': visual_stories,
        'ads': ads,
        'video_ads': video_ads
    }

    return render(request, 'video_and_visual_stories.html', context)

@login_required(login_url='login')
@user_passes_test(regular_user_check, login_url='login')
def preferred_news(request):
    profile = Profile.objects.get(user=request.user)
    
    # Get all subcategories related to the user's preferred categories
    categories = [profile.category1, profile.category2, profile.category3]
    ads = ImageAds.objects.all()  # Fetch all advertisement images
    video_ads = VideoAds.objects.all().order_by('-id')
    latest_news = NewsArticle.objects.order_by('-id')[:10]
    
    subcategories = SubCategory.objects.filter(category__in=categories).distinct()
    news_by_subcategory = {}
    
    for subcategory in subcategories:
        news_by_subcategory[subcategory] = NewsArticle.objects.filter(subcategory=subcategory)
    
    context = {
        'news_by_subcategory': news_by_subcategory,
        'ads': ads,
        'video_ads': video_ads,
        'latest_news' : latest_news
    }
    return render(request, 'preferred_news.html', context)

@login_required(login_url='login')
@user_passes_test(regular_user_check, login_url='login')
def update_preferences(request):
    profile = Profile.objects.get(user=request.user)
    ads = ImageAds.objects.all()  # Fetch all advertisement images
    latest_news = NewsArticle.objects.order_by('-id')[:6]
    if request.method == "POST":
        category1 = request.POST.get('category1')
        category2 = request.POST.get('category2')
        category3 = request.POST.get('category3')
        
        try:
            profile.category1 = Category.objects.get(id=category1) if category1 else None
            profile.category2 = Category.objects.get(id=category2) if category2 else None
            profile.category3 = Category.objects.get(id=category3) if category3 else None
            profile.save()
            messages.success(request, 'Prefernce updated successfully!')
            return redirect('preferred_news')  # Redirect to a page that shows updated preferences
        except Category.DoesNotExist:
            return HttpResponse("Selected category does not exist.", status=400)
    
    # Fetch all categories for the dropdown
    categories = Category.objects.all()
    
    context = {
        'profile': profile,
        'categories': categories,
        'ads': ads,
        'latest_news' : latest_news
    }
    
    return render(request, 'update_preferences.html', context)


# View to display news articles for a subcategory
def subcategory_news_view(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    articles = NewsArticle.objects.filter(subcategory=subcategory)
    ads = ImageAds.objects.all()  # Fetch all advertisement images
    video_ads = VideoAds.objects.all().order_by('-id')
    return render(request, 'subcategory_news.html', {'subcategory': subcategory, 'articles': articles, 'ads':ads, 'video_ads':video_ads})

def search_results(request):
    query = request.GET.get('q')
    visual_stories = VisualStory.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query))
    visual_stories = visual_stories.order_by('-id')
    video_news = VideoNews.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query))
    video_news = video_news.order_by('-id')
    news_articles = NewsArticle.objects.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(location__icontains=query))
    news_articles = news_articles.order_by('-id')
    ads = ImageAds.objects.all()  # Fetch all advertisement images
    video_ads = VideoAds.objects.all().order_by('-id')

    context = {
        'query': query,
        'visual_stories': visual_stories,
        'video_news': video_news,
        'news_articles': news_articles,
        'ads':ads,
        'video_ads':video_ads
        
    }

    return render(request, 'search_results.html', context)

def regional_view(request):
    # Get unique locations for each level
    all_countries = set()
    filtered_states = set()
    filtered_cities = set()

    # Collect unique locations from all models
    visual_story_locations = VisualStory.objects.values_list('location', flat=True)
    news_article_locations = NewsArticle.objects.values_list('location', flat=True)
    video_news_locations = VideoNews.objects.values_list('location', flat=True)
    ads = ImageAds.objects.all()  # Fetch all advertisement images
    video_ads = VideoAds.objects.all().order_by('-id')

    # Combine all locations into a set for uniqueness
    all_locations = list(visual_story_locations) + list(news_article_locations) + list(video_news_locations)

    # Loop through all locations and populate sets for countries, states, and cities
    for loc in all_locations:
        if loc:
            location_parts = loc.split('-')
            if len(location_parts) >= 1:
                all_countries.add(location_parts[0])
            if len(location_parts) >= 2:
                if request.GET.get('country') == location_parts[0]:  # Only add states belonging to the selected country
                    filtered_states.add(location_parts[1])
            if len(location_parts) >= 3:
                if request.GET.get('country') == location_parts[0] and request.GET.get('state') == location_parts[1]:  # Only add cities belonging to the selected state
                    filtered_cities.add(location_parts[2])

    # Retrieve selected filters from the request
    selected_country = request.GET.get('country')
    selected_state = request.GET.get('state')
    selected_city = request.GET.get('city')

    # Filter the entries based on the selected location
    if selected_city:
        visual_stories = VisualStory.objects.filter(location__icontains=f"{selected_country}-{selected_state}-{selected_city}")
        news_articles = NewsArticle.objects.filter(location__icontains=f"{selected_country}-{selected_state}-{selected_city}")
        video_news = VideoNews.objects.filter(location__icontains=f"{selected_country}-{selected_state}-{selected_city}")
    elif selected_state:
        visual_stories = VisualStory.objects.filter(location__icontains=f"{selected_country}-{selected_state}")
        news_articles = NewsArticle.objects.filter(location__icontains=f"{selected_country}-{selected_state}")
        video_news = VideoNews.objects.filter(location__icontains=f"{selected_country}-{selected_state}")
    elif selected_country:
        visual_stories = VisualStory.objects.filter(location__icontains=selected_country)
        news_articles = NewsArticle.objects.filter(location__icontains=selected_country)
        video_news = VideoNews.objects.filter(location__icontains=selected_country)
    else:
        visual_stories = None
        news_articles = None
        video_news = None

    context = {
        'countries': sorted(all_countries),
        'states': sorted(filtered_states),
        'cities': sorted(filtered_cities),
        'selected_country': selected_country,
        'selected_state': selected_state,
        'selected_city': selected_city,
        'visual_stories': visual_stories,
        'news_articles': news_articles,
        'video_news': video_news,
        'ads':ads,
        'video_ads':video_ads
    }

    return render(request, 'regional_page.html', context)

def regional_news_state(request, state):
    selected_city = 'All'
    
    if state != "All":
        visual_stories = VisualStory.objects.filter(location__contains=f'-{state}-').exclude(location__startswith="International")
        video_news = VideoNews.objects.filter(location__contains=f'-{state}-').exclude(location__startswith="International")
        news_articles = NewsArticle.objects.filter(location__contains=f'-{state}-').exclude(location__startswith="International")
    else:
        visual_stories = VisualStory.objects.exclude(location__startswith="International").exclude(location__isnull=True)
        video_news = VideoNews.objects.exclude(location__startswith="International").exclude(location__isnull=True)
        news_articles = NewsArticle.objects.exclude(location__startswith="International").exclude(location__isnull=True)
    
    context = {
        'visual_stories': visual_stories,
        'video_news': video_news,
        'news_articles': news_articles,
        'all_states': get_all_states(),
        'all_cities': get_all_cities(),
        'selected_state': state,
        'selected_city': selected_city,
    }
    return render(request, 'regional_news.html', context)


def regional_news_city(request, city):
    selected_state = 'All'

    if city != "All":
        visual_stories = VisualStory.objects.filter(location__endswith=f'-{city}').exclude(location__startswith="International")
        video_news = VideoNews.objects.filter(location__endswith=f'-{city}').exclude(location__startswith="International")
        news_articles = NewsArticle.objects.filter(location__endswith=f'-{city}').exclude(location__startswith="International")
    else:
        visual_stories = VisualStory.objects.exclude(location__startswith="International").exclude(location__isnull=True)
        video_news = VideoNews.objects.exclude(location__startswith="International").exclude(location__isnull=True)
        news_articles = NewsArticle.objects.exclude(location__startswith="International").exclude(location__isnull=True)
    
    context = {
        'visual_stories': visual_stories,
        'video_news': video_news,
        'news_articles': news_articles,
        'all_states': get_all_states(),
        'all_cities': get_all_cities(),
        'selected_state': selected_state,
        'selected_city': city,
    }
    return render(request, 'regional_news.html', context)

def regional_news(request):
    # Fetch all visual stories, video news, and news articles that don't start with "International"
    visual_stories = VisualStory.objects.exclude(location__startswith="International").exclude(location__isnull=True)
    video_news = VideoNews.objects.exclude(location__startswith="International").exclude(location__isnull=True)
    news_articles = NewsArticle.objects.exclude(location__startswith="International").exclude(location__isnull=True)

    # Context data: including lists of all available states and cities
    context = {
        'visual_stories': visual_stories,
        'video_news': video_news,
        'news_articles': news_articles,
        'all_states': get_all_states(),
        'all_cities': get_all_cities(),
        'selected_state': 'All',  # No state selected
        'selected_city': 'All',   # No city selected
    }
    return render(request, 'regional_news.html', context)

def get_all_states():
    # Extract unique state names from the location field
    states = set()
    for story in VisualStory.objects.exclude(location__isnull=True):
        location_parts = story.location.split('-')
        if len(location_parts) >= 2 and location_parts[0] != "International":
            states.add(location_parts[1])
    return sorted(states)


def get_all_cities():
    # Extract unique city names from the location field
    cities = set()
    for story in VisualStory.objects.exclude(location__isnull=True):
        location_parts = story.location.split('-')
        if len(location_parts) == 3 and location_parts[0] != "International":
            cities.add(location_parts[2])
    return sorted(cities)

@login_required(login_url='login')
@user_passes_test(regular_user_check, login_url='login')
def save_article(request, article_id):
    article = get_object_or_404(NewsArticle, id=article_id)
    profile = request.user.profile

    if article in profile.saved_articles.all():
        profile.saved_articles.remove(article)  # Unsave if already saved
        saved = False
    else:
        profile.saved_articles.add(article)  # Save the article
        saved = True

    return JsonResponse({'saved': saved})

@login_required(login_url='login')
@user_passes_test(regular_user_check, login_url='login')
def saved_articles(request):
    profile = request.user.profile
    saved_articles = profile.saved_articles.all()  # Get all saved articles for the user
    saved_videos = profile.saved_videos.all()

    return render(request, 'saved_articles.html', {'saved_articles': saved_articles, 'saved_videos': saved_videos})

@login_required(login_url='login')
@user_passes_test(regular_user_check, login_url='login')
def save_video(request, video_id):
    video = get_object_or_404(VideoNews, id=video_id)
    profile = request.user.profile

    if video in profile.saved_videos.all():
        profile.saved_videos.remove(video)
        saved = False
    else:
        profile.saved_videos.add(video)
        saved = True

    return JsonResponse({'saved': saved})