from django.contrib import admin
from django.urls import path

from .views import (
  PollListView,
  PollDetailView,
  poll_create,
  choice_create,
  number_options,
  vote,
)

app_name = 'polls'
urlpatterns = [
  path('', PollListView.as_view(), name='polls'),
  path('create/', poll_create, name="poll-create"),
  path('create/numer-of-options/', number_options, name="option-number"),
  path('create/add-choice/', choice_create, name="choice-create"),
  path('poll/<int:pk>/', PollDetailView.as_view(), name='poll-detail'),
  path('poll/<int:pk>/vote/', vote, name='poll-vote'),
  # path('ui/', ui, name="ui")

]