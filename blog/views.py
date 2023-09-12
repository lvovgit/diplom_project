from django.shortcuts import render
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


def last_post(request):
    posts = Post.objects.order_by("-create_at")[0:3]
    response_data = {
        'posts': posts,
    }
    return render(request, 'main/card_last_post.html', response_data)



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
