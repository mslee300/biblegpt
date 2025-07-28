from django.shortcuts import render
from openai import OpenAI
import os

from .forms import AnswerForm

client = OpenAI(api_key=os.environ['OPENAI'])


# AI message generator
def generate_message(request, prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        max_tokens=600,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        messages=[{
            "role":
            "user",
            "content":
            f"You are an expert in the Bible. Answer questions using biblical verses. If the Bible does not explicitly address the question, reply with 'The Bible does not explicitly say,' and suggest a related verse. For inappropriate or offensive questions, respond with 'This question does not align with biblical teachings.' Always provide the verse, chapter, and book name when citing. Question: {prompt}"
        }])
    return response.choices[0].message.content


# Main page
def index(request):
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            question = form['prompt'].value()
            message = generate_message(request, form['prompt'].value())
            context = {
                'question': question,
                'message': message,
            }
        return render(request, 'answer.html', context)
    else:
        form = AnswerForm()

    return render(request, "kist.html", {"form": form})
