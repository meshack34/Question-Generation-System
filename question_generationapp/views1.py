# question_generationapp/views.py
from django.http import JsonResponse


# question_generationapp/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .forms import TextForm
from .trainer.qg_train import train_question_generation_model
from .trainer.qa_eval_train import evaluate_question_generation_model

def generate_question_view(request):
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            model = train_question_generation_model(text) 
            print(model)
            print(text) # Train the model if needed
            question = evaluate_question_generation_model(model, text)
            return JsonResponse({'question': question})
    else:
        form = TextForm()
    return render(request, 'question_generationapp/generate_question.html', {'form': form})
