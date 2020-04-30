from django.urls import path
from . import views

app_name=  'blog'

urlpatterns = [
    path('new/', views.NewBlogView.as_view(), name="new-blog"),
    path('update/<int:pk>/', views.UpdateBlogView.as_view(), name="update-blog"),
    path('post/new/', views.BlogPostView.as_view(), name="new-blog-post"),
    path('post/<int:pk>/update/', views.BlogPostUpdateView.as_view(), name="update-blog-post"),
    path('post/<int:pk>/detail/', views.BlogPostDetailView.as_view(), name="detail-blog-post"),
    path('post/<int:pk>/share/', views.ShareBlogPostView.as_view(), name="share-blog-post-with-blog"),
    path('post/<int:post_pk>/share/<int:blog_pk>/', views.SharePostWithBlog.as_view(), name="share-post-with-blog"),
    path('post/<int:post_pk>/stop/share/to/<int:blog_pk>/', views.StopSharingPostWithBlog.as_view(), name="stop-sharing-post-with-blog"),
]

