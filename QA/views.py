from django.shortcuts import render
# Create your views here.
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.safestring import mark_safe
from utils import agent


def index(request):
    return render(request, 'index.html')


@xframe_options_exempt
def user(request):
    if request.method == 'GET':
        return render(request, 'pages/user.html')
    else:
        question = request.POST['question']
        answer = agent.run(question)
        if answer:
            context = {'answer': answer}
        else:
            context = {'answer': '更多功能计划开发中敬请期待'}
        li = "<li class='left'><div class='left-img'><img src='../static/images/agent.png' alt=""></div><div " \
             "class='left-inf'>" + context['answer'] + "</div><br></li> "
        context['li'] = mark_safe(li)
        return render(request, "pages/user.html", context)
