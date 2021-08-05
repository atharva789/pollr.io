from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import get_object_or_404

# Create your models here.
class Poll(models.Model):
  question = models.CharField(max_length=250)
  creator = models.CharField(max_length=100)
  # pub_date = models.DateTimeField(auto_now_add=True)
  description = models.CharField(max_length=120)
  #options --> point to options database table
  #option_votes --> point to options database table

  def recent(self):
    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
  

  def __str__(self):
    return self.question

  def get_absolute_url(self):
	  return reverse("polls:poll-detail", kwargs={"pk": self.id})

  # def sort_vote_choices(self):
  #   sorted_options = {
  #     Poll.objects.all():Poll.objects.all().choice_set.all().order_by('option_votes')
  #     }
  #   return sorted_options
class Choice(models.Model):
  poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
  option = models.CharField(max_length=200)
  option_votes = models.IntegerField(default=0)

  def __str__(self):
    return self.option

