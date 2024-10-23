from django.urls import path
from .import views

urlpatterns = [
    

    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('ad-manage-categorys/', views.manage_categorys, name='manage_categorys'),
    path('ad-delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('ad-add-category/', views.add_category, name='add_category'),
    path('ad-add-visual-story/', views.add_visual_story, name='add_visual_story'),
    path('ad-visual-stories/', views.visual_story_list, name='visual_story_list'),  # List view
    path('ad-edit-visual-story/<int:story_id>/', views.edit_visual_story, name='edit_visual_story'),  # Edit view
    path('ad-delete-visual-story/<int:story_id>/', views.delete_visual_story, name='delete_visual_story'),  # Delete view
    path('ad-add-video-news/', views.add_video_news, name='add_video_news'),
    path('ad-video-news/', views.video_news_list, name='video_news_list'),
    path('ad-video-news/edit/<int:video_id>/', views.edit_video_news, name='edit_video_news'),
    path('ad-video-news/delete/<int:video_id>/', views.delete_video_news, name='delete_video_news'),
    path('ad-subcategories/', views.subcategory_view, name='subcategory-list'),
    path('ad-subcategories/delete/<int:pk>/', views.delete_subcategory, name='subcategory-delete'),
    path('ad-news/add/', views.add_news_article, name='add-news-article'),
    path('ad-news/', views.list_news_articles, name='list_news_articles'),
    path('ad-news/delete/<int:article_id>/', views.delete_news_article, name='delete-news-article'),
    path('ad-news/edit/<int:article_id>/', views.edit_news_article, name='edit-news-article'),
    path('ad-video-ads/add/', views.add_video_ad, name='add_video_ad'),
    path('ad-video-ads/', views.list_video_ads, name='list_video_ads'),
    path('ad-video-ads/edit/<int:ad_id>/', views.edit_video_ad, name='edit_video_ad'),
    path('ad-video-ads/delete/<int:ad_id>/', views.delete_video_ad, name='delete-video-ad'),
    path('ad-imageadd-ad/', views.add_image_ad, name='add_image_ad'),
    path('ad-listads/', views.list_image_ads, name='list_image_ads'),
    path('ad-ads/edit/<int:ad_id>/', views.edit_image_ad, name='edit_image_ad'),
    path('front_page', views.front_page, name='front_page'),
    path('news/<int:article_id>/', views.news_detail, name='news_detail'),  # Detailed news view
    path('videos/<int:video_id>/', views.video_detail, name='video_detail'),
    path('visual-story/<int:visual_story_id>/', views.story_card_detail, name='story_card_detail'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('news-by-category/', views.news_by_category, name='news_by_category'),
    path('media/', views.video_and_visual_stories, name='video_and_visual_stories'),
    ######################################################################################################################
    path('ajax/check_username/', views.check_username, name='check_username'),
    path('ajax/check_email/', views.check_email, name='check_email'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('lgout',views.lgout,name='lgout'),
    ######################################################################################################################
    path('preferred-news/', views.preferred_news, name='preferred_news'),
    path('update-preferences/', views.update_preferences, name='update_preferences'),
    path('subcategory/<int:subcategory_id>/', views.subcategory_news_view, name='subcategory_news'),
    path('search/', views.search_results, name='search_results'),
    path('regional/', views.regional_view, name='regional'),
    path('regional-news/', views.regional_news, name='regional_news'),
    path('regional-news/state/<str:state>/', views.regional_news_state, name='state_news'),
    path('regional-news/city/<str:city>/', views.regional_news_city, name='city_news'),
    path('save-article/<int:article_id>/', views.save_article, name='save_article'),
    path('saved-articles/', views.saved_articles, name='saved_articles'),
    path('save-video/<int:video_id>/', views.save_video, name='save_video'),
    



    

]