# question_generationapp/model_utils.py
import torch
from transformers import T5Tokenizer

# question_generationapp/model_utils.py
from transformers import T5ForConditionalGeneration, T5Tokenizer

def load_trained_model(model_path):
    model = T5ForConditionalGeneration.from_pretrained(model_path)
    return model

def evaluate_question_generation_model(model, text):
    tokenizer = T5Tokenizer.from_pretrained("t5-small")
    inputs = tokenizer.encode_plus(text, add_special_tokens=True, return_tensors="pt")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    inputs = inputs.to(device)

    with torch.no_grad():
        output = model.generate(input_ids=inputs["input_ids"], max_length=50, num_beams=4, early_stopping=True)

    question = tokenizer.decode(output[0], skip_special_tokens=True)
    return question
