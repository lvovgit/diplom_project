from django.urls import path

from . import views

# from django.views.decorators.cache import cache_page


urlpatterns = [
    path('comment/<int:pk>/', views.CreateComment.as_view(), name="create_comment"),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name="post_detail"),
    path('<slug:slug>/', views.PostCategoryListView.as_view(), name="post_category_list"),
    path('', views.PostListView.as_view(), name="post_list"),
    # # path('', cache_page(60 * 15)(views.HomeView.as_view()), name="home"),

]
