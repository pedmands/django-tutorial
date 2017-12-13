from django.contrib import admin

# Register your models here.
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
	search_fields = ['question_text']
	list_filter = ['pub_date']
	list_display = ('question_text', 'pub_date', 'was_published_recently', 'get_choices')
	fieldsets = [
		(None,               {'fields': ['question_text']}),
		('Date information', {'fields': ['pub_date']}),
	]
	inlines = [ChoiceInline]
	def get_choices(self, obj):
		c = obj.choice_set.all()
		return list(c)
	get_choices.short_description = "Choices"

admin.site.register(Question, QuestionAdmin)




