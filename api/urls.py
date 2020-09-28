from django.urls import path
from .views import SingleMessageView, MessagesView

urlpatterns = [
    path('api/v1/messages/<int:pk>', SingleMessageView.as_view()),
    path('api/v1/messages/', MessagesView.as_view())
]
