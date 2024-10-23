# In context_processors.py
from .models import Category
from django.utils import timezone
from django.db.models import Count
from .models import VisualStory, StoryCard, Category, VideoNews, SubCategory, NewsArticle, VideoAds, ImageAds, Profile, Comment

def categories_processor(request):
    categories = Category.objects.all()
    last_updated_time =  timezone.now()
    categoriess = Category.objects.annotate(subcategory_count=Count('subcategories')).filter(subcategory_count__gt=0)
    aavisual_stories = VisualStory.objects.order_by('-id')[:10]
    aavideo_news_list = VideoNews.objects.order_by('-id')[:10]
    aanews_articles = NewsArticle.objects.order_by('-id')[:10]
    return {'categories': categories, 'last_updated_time': last_updated_time.strftime('%b %d, %Y, %I:%M %p'), 'categoriess': categoriess,
             'aavisual_stories': aavisual_stories, 'aavideo_news_list': aavideo_news_list, 'aanews_articles': aanews_articles}
