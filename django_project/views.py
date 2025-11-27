from django.shortcuts import render
from openai import OpenAI
import os

from .forms import AnswerForm

# Initialize OpenAI client - set OPENAI_API_KEY environment variable
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY', 'your-key-here'))


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
            f"당신은 성경 전문가입니다. 모든 질문에 성경 구절을 활용하여 답변하세요. 성경에서 직접적으로 다루지 않는 내용이라면 '성경에 명확한 언급이 없습니다.'라고 답하고, 관련된 성경 구절을 제시하세요. 부적절하거나 불건전한 질문일 경우 '이 질문은 성경의 가르침에 부합하지 않습니다.'라고 답변하세요. 성경 구절을 인용할 때는 반드시 책 이름, 장, 절을 함께 제시하세요. 질문: {prompt}"
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
