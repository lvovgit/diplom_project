from django.urls import path

from main.apps import MainConfig
from main.views import home, FeedbackCreateView, FeedbackSuccessView

app_name = MainConfig.name
urlpatterns = [

    path('', home, name='home'),
    # path('contacts/', contacts, name='contacts'),

    path('feedback/', FeedbackCreateView.as_view(), name='feedback'),
    path('feedback_success/', FeedbackSuccessView.as_view(), name='feedback_success'),
    ]