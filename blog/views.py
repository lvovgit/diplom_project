from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, CreateView, ListView
from taggit.models import Tag

from .forms import CommentForm
from .models import Post, Comment


class PostListView(ListView):
    """Вывод списка постов"""
    model = Post
    extra_context = {
        'object_list': Post.objects.all(),

    }

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = queryset.filter(published=True)
        return queryset


class PostCategoryListView(ListView):
    """Вывод списка постов по категориям"""
    model = Post

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs.get("slug")).select_related('category')


class PostByTagListView(ListView):
    """Вывод списка постов по тегам"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    tag = None

    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs['tag'])
        queryset = Post.objects.all().filter(tags__slug=self.tag.slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Статьи по тегу: {self.tag.name}'
        return context


class PostDetailView(DetailView):
    """Детальный вывод поста"""
    model = Post
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        obj = self.get_object()
        increase = get_object_or_404(Post, pk=obj.pk)
        increase.increase_views()
        return context


class CreateComment(CreateView):
    """Реализация создания комментария"""
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs.get('pk')
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()

# class PostSearchView(ListView):
#     """
#     Реализация поиска статей на сайте
#     """
#     model = Post
#     context_object_name = 'posts'
#     paginate_by = 5
#     template_name = 'blog/post_list.html'
#
#     def get_queryset(self):
#         return Post.objects.filter(slug__icontains=self.request.GET.get('q'))
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['q'] = f'Результаты поиска: {self.request.GET.get("q")}'
#         return context
