from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, CreateView, ListView
from taggit.models import Tag

from .forms import CommentForm
from .models import Post, Comment


class PostListView(ListView):
    model = Post
    extra_context = {
        'object_list': Post.objects.all(),

    }

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = queryset.filter(published=True)
        return queryset


class PostCategoryListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs.get("slug")).select_related('category')

class PostByTagListView(ListView):
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
    model = Post
    context_object_name = "post"
    # slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        obj = self.get_object()
        increase = get_object_or_404(Post, pk=obj.pk)
        increase.increase_views()
        return context


class CreateComment(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs.get('pk')
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class PostSearchResultView(ListView):
    """
    Реализация поиска статей на сайте
    """
    model = Post
    context_object_name = 'articles'
    paginate_by = 10
    allow_empty = True
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        query = self.request.GET.get('do')
        search_vector = SearchVector('full_description', weight='B') + SearchVector('title', weight='A')
        search_query = SearchQuery(query)
        return (self.model.objects.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by('-rank'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Результаты поиска: {self.request.GET.get("do")}'
        return context