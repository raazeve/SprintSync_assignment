# views.py
import json
from django.conf import settings
import openai
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def daily_plan(request):
    """
    Calls OpenAI to generate a daily plan based on the user's incomplete tasks.
    """
    # 1. Fetch the user's tasks that are not done
    tasks = Task.objects.filter(assigned_to=request.user).exclude(status='DONE')
    task_list = [f"- {task.title} ({task.status})" for task in tasks]

    # 2. Construct the prompt
    prompt = f"""
    User {request.user.username} has the following tasks for today:
    "\n".join(task_list)

    Please generate a concise, actionable daily plan. Prioritize 'IN_PROGRESS' tasks.
    Suggest an order to tackle them and estimate a rough timeline.
    Return the response in a clear JSON format with two fields: 'plan' (string) and 'estimated_hours' (number).
    """

    # 3. Call OpenAI (with error handling)
    try:
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" } # Crucial for deterministic JSON
        )
        ai_content = response.choices[0].message.content
        return Response(json.loads(ai_content))

    except Exception as e:
        # Graceful degradation: Return a stub response if AI call fails
        stub_response = {
            "plan": "Complete all tasks in order of priority. Focus on in-progress items first.",
            "estimated_hours": 4
        }
        return Response(stub_response, status=503)