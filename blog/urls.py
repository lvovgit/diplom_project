from django.urls import path
from . import views

urlpatterns = [
    path('comment/<int:pk>/', views.CreateComment.as_view(), name="create_comment"),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name="post_detail"),
    path('<slug:slug>/', views.PostCategoryListView.as_view(), name="post_category_list"),
    path('posts/tags/<str:tag>/', views.PostByTagListView.as_view(), name='post_by_tags'),
    path('', views.PostListView.as_view(), name="post_list"),

]
