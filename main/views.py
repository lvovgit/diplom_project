from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import FeedbackCreateForm
from .models import Feedback
from .services.email import send_contact_email_message


# Create your views here.

def home(request):

    return render(request, 'main/home.html')




class FeedbackCreateView(SuccessMessageMixin, CreateView):
    model = Feedback
    form_class = FeedbackCreateForm
    success_message = 'Ваше письмо успешно отправлено администрации сайта'
    template_name = 'main/email/feedback.html'
    # extra_context = {'title': 'Контактная форма'}
    success_url = reverse_lazy('main:feedback_success')

    def form_valid(self, form):
        if form.is_valid():
            feedback = form.save(commit=False)
            if self.request.user.is_authenticated:
                feedback.user = self.request.user
            send_contact_email_message(feedback.subject, feedback.email, feedback.content, feedback.user_id, )
        return super().form_valid(form)


class FeedbackSuccessView(TemplateView):
    template_name = 'main/email/feedback_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваше письмо отправлено администрации сайта'
        return context