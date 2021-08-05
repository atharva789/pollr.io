from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

# Create your views here.
from .models import (
  Poll,
  Choice
)

from django.views.generic import (
  ListView,
  DetailView,
  CreateView, 
  UpdateView,
  DeleteView
)

from .forms import (PollForm, ChoiceForm, ManyOptionsForm)
from django.forms import formset_factory
# from django.views.generic.edit import (
#   CreateView, 
#   UpdateView,
#   DeleteView
# )
app_name = 'polls'
n = 0
class PollListView(ListView):
  model = Poll
  template_name = 'polls.html'
  queryset = Poll.objects.all()

  def get_object(self):
    id_ = self.kwargs.get("pk")
    return get_object_or_404(Poll, id=id_)

  def get_context_data(self, **kwargs):
    polls = Poll.objects.all()
    context = super().get_context_data(**kwargs)
    context['poll_list'] = polls
    for poll in polls:
      poll.choice_set.all().order_by('option_votes')
      filtered_options = poll.choice_set.all().order_by('option_votes')
      context['sorted_votes'] = {poll.id: filtered_options}
    return context

def poll_create(request):
  if request.method == 'POST':
    form = PollForm(request.POST)
    # multiple_form = ManyOptionsForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('polls:option-number')
  else:
    form = PollForm()
  return render(request, 'poll-create.html', {'question_form': form})

def number_options(request):
  multiple_form = ManyOptionsForm()
  if request.method == 'POST':
    multiple_form = ManyOptionsForm(request.POST)
    if multiple_form.is_valid():
      print(multiple_form.cleaned_data)
      # multiple_form.save()
      return redirect('polls:choice-create')
  else:
    multiple_form = ManyOptionsForm()
  return render(request, 'decide-option_number.html', {'form':multiple_form})

def choice_create(request):
  number_of_options = 1
  filled_multiple_options_form = ManyOptionsForm(request.POST)

  if filled_multiple_options_form.is_valid():
    number_of_options = filled_multiple_options_form.cleaned_data['number']

  OptionFormSet = formset_factory(ChoiceForm, extra=number_of_options)
  formset = OptionFormSet()

  queryset = Poll.objects.all()
  queryset = list(queryset)[-1]
  if request.method == 'POST':
    filled_formset = OptionFormSet(request.POST)
    if filled_formset.is_valid():
      for form in filled_formset:
        form.save()
      messages.success(request, 'poll created sucessfully!')
      return redirect('polls:polls')
  else:
    formset = OptionFormSet()
  return render(request, 'choice_create.html', {'formset': formset,'poll': queryset})


class PollDetailView(DetailView):
  model = Poll
  template_name = 'poll-detail.html'
  queryset = Poll.objects.all()

  def get_object(self):
    id_ = self.kwargs.get("pk")
    return get_object_or_404(Poll, id=id_)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data()

    if len(self.get_object().choice_set.filter(option_votes=0))==len(self.get_object().choice_set.all()):
      not_voted = True
      context['not_voted'] = not_voted
    else:
      not_voted = False
      context['not_voted'] = not_voted
    
    return context
  # def get_context_data(self, **kwargs):
  #   context = super().get_context_data(**kwargs)

  #   zero_votes = list(Choice.objects.filter(option_votes=0)

  #   if len(zero_votes) == len(self.get_object.choice_set.all()):
  #     not_voted = True
  #     context['unvoted_list'] = zero_votes
  #   else:
  #     not_voted = False
  #     context['voted_list'] = voted
  #   return context
    
def vote(request, pk):
  question = get_object_or_404(Poll, pk=pk)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    # Redisplay the question voting form.
    return render(request, 'poll-vote.html', {
      'question': question,
      'error_message': "You didn't select a choice.",
    })
  else:
    selected_choice.option_votes += 1
    selected_choice.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return redirect('polls:poll-detail', question.id)

def ui(request):
  return render(request,'ui-test.html')