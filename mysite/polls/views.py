from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		global i
		
		"""
		Return the last five published questions
		(not including those set to be published in the future),
		(and not including those without at least one choice). -- !! To Implement !! --
		"""
		q_list = []
		i = 1

		for q in Question.objects.all():
			if q.choice_set.exists():
				q_list.append(q)

		q_list_filtered = list(filter(lambda q: q.pub_date <= timezone.now(), q_list))

		return q_list_filtered

		# return Question.objects.filter(
		# 		pub_date__lte=timezone.now() # and
		# 		# len(list(choice_set.all())) > 0
		# 		).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

	def get_queryset(self):
		"""Excludes any questions that aren't published yet."""
		return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

	def get_queryset(self):
		"""Excludes any questions that aren't published yet"""
		return Question.objects.filter(pub_date__lte=timezone.now())

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except:
		# Redisplay the question voting form.
		return render(request, 'polls/detail.html', {
			'question' : question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))