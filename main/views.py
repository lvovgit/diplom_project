from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from blog.models import Post
from .forms import FeedbackCreateForm
from .models import Feedback
from .services.email import send_contact_email_message


def home(request):
    """Вывод основной страницы"""
    extra_context = {
        'post_list': Post.objects.order_by("-view_count")[0:1],
        'post_list_2': Post.objects.order_by("-view_count")[1:3],
        'main_post': Post.objects.order_by('-view_count').first(),
        'main_posts': Post.objects.order_by('-view_count')[1:],
        'other_posts': Post.objects.order_by('-view_count')

    }
    return render(request, 'main/home.html', extra_context)


class FeedbackCreateView(SuccessMessageMixin, CreateView):
    """Реализация заполнения формы фидбека"""
    model = Feedback
    form_class = FeedbackCreateForm
    success_message = 'Ваше письмо успешно отправлено администрации сайта'
    template_name = 'main/email/feedback.html'
    success_url = reverse_lazy('main:feedback_success')

    def form_valid(self, form):
        if form.is_valid():
            feedback = form.save(commit=False)
            send_contact_email_message(feedback.subject, feedback.email, feedback.content, feedback.user_id, )
        return super().form_valid(form)


class FeedbackSuccessView(TemplateView):
    """Реализация успешного заполнения формы фидбека"""
    template_name = 'main/email/feedback_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваше письмо отправлено администрации сайта'
        return context
