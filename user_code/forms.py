from django.forms import ModelForm
from user_code.models import Result
from django import forms

class ResultForm(ModelForm):
  class Meta:
      model = Result
      fields = ['forest_errors', 'forest_plots', 'forest_results']
