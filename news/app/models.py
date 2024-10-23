from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class VisualStory(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='visual_stories')  # Add Category ForeignKey
    published_date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, blank=True, null=True, default=None)

    def __str__(self):
        return self.title

class StoryCard(models.Model):
    visual_story = models.ForeignKey(VisualStory, related_name='story_cards', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/story_images/')
    heading = models.CharField(max_length=255)
    short_text = models.TextField(max_length=500)

    def __str__(self):
        return self.heading
    

class VideoNews(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    video = models.FileField(upload_to='media/videos/')
    location = models.CharField(max_length=255, blank=True, null=True, default=None)

    def __str__(self):
        return self.title
    
class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/article_images/')
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE, related_name='articles')
    reporter = models.CharField(max_length=100)  # Assuming reporter name is a simple text field
    location = models.CharField(max_length=255, blank=True, null=True, default=None)

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name



    

class VideoAds(models.Model):
    video = models.FileField(upload_to='media/video_ads/')
    company = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.company} - {self.description[:50]}"
    

class ImageAds(models.Model):
    company = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='media/ads_images/')
    link = models.URLField(max_length=500, blank=True, null=True)  # New field for the ad link
    
    def __str__(self):
        return self.company


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_articles = models.ManyToManyField(NewsArticle, blank=True)
    saved_videos = models.ManyToManyField(VideoNews, blank=True)  # Add this
    phone = models.CharField(max_length=15)
    address = models.TextField()
    category1 = models.ForeignKey(Category, related_name='category1', on_delete=models.SET_NULL, null=True)
    category2 = models.ForeignKey(Category, related_name='category2', on_delete=models.SET_NULL, null=True)
    category3 = models.ForeignKey(Category, related_name='category3', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username
    


class Comment(models.Model):
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.article.title}'