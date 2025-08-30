import json
import logging
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Task
from .serializers import ( 
    TaskSerializer, 
    TaskStatusUpdateSerializer,
    AIDailyPlanRequestSerializer
)

# AI imports
import openai
from openai import APIConnectionError, APIError, RateLimitError
from django.conf import settings

logger = logging.getLogger(__name__)
User = get_user_model()

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Users can see tasks they created or are assigned to
        if user.is_admin:
            return Task.objects.all()
        return Task.objects.filter(
            Q(created_by=user) | Q(assigned_to=user)
        )

    @action(detail=True, methods=['patch'], serializer_class=TaskStatusUpdateSerializer)
    def status(self, request, pk=None):
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AIViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def daily_plan(self, request):
        """
        Generate a daily plan for the authenticated user using AI
        """
        # Validate request data if needed
        serializer = AIDailyPlanRequestSerializer(data=request.data)
        if serializer.is_valid() or not request.data:  # Allow empty requests
            user = request.user
            
            # Get user's tasks that are not done
            tasks = Task.objects.filter(
                Q(created_by=user) | Q(assigned_to=user)
            ).exclude(status=Task.Status.DONE)
            
            # Prepare task list for the prompt
            task_list = []
            for task in tasks:
                task_list.append({
                    "title": task.title,
                    "status": task.status,
                    "time_estimate": task.total_minutes
                })
            
            # Construct the prompt
            prompt = f"""
            User {user.username} has the following tasks for today:
            {json.dumps(task_list, indent=2)}
            
            Please generate a concise, actionable daily plan. Prioritize 'IN_PROGRESS' tasks.
            Suggest an order to tackle them and estimate a rough timeline.
            Return the response in a clear JSON format with two fields: 'plan' (string) and 'estimated_hours' (number).
            """
            
            # Call OpenAI API with enhanced error handling
            try:
                if not settings.OPENAI_API_KEY:
                    logger.warning("OpenAI API key not configured, using fallback response")
                    return self._get_fallback_response()
                    
                client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={ "type": "json_object" }
                )
                
                ai_content = response.choices[0].message.content
                return Response(json.loads(ai_content))
                
            except RateLimitError as e:
                logger.warning(f"OpenAI rate limit exceeded: {str(e)}")
                return self._get_fallback_response()
                
            except (APIConnectionError, APIError) as e:
                logger.warning(f"OpenAI API error: {str(e)}")
                return self._get_fallback_response()
                
            except Exception as e:
                logger.error(f"Unexpected error in AI API: {str(e)}", exc_info=True)
                return self._get_fallback_response()
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        # Add this method to your AIViewSet class
    def _generate_local_plan(self, user):
        """Generate a simple daily plan using local logic"""
        tasks = Task.objects.filter(
            Q(created_by=user) | Q(assigned_to=user)
        ).exclude(status=Task.Status.DONE)
        
        # Simple prioritization logic
        in_progress_tasks = [t for t in tasks if t.status == Task.Status.IN_PROGRESS]
        todo_tasks = [t for t in tasks if t.status == Task.Status.TO_DO]
        
        plan_parts = []
        
        if in_progress_tasks:
            plan_parts.append("First, continue working on your in-progress tasks:")
            for task in in_progress_tasks:
                plan_parts.append(f"- {task.title} (already started)")
        
        if todo_tasks:
            if in_progress_tasks:
                plan_parts.append("Then, tackle these new tasks:")
            else:
                plan_parts.append("Start with these tasks:")
            
            for task in todo_tasks:
                plan_parts.append(f"- {task.title}")
        
        if not plan_parts:
            plan_parts.append("No pending tasks. Great job!")
        
        # Estimate total time (simple heuristic)
        total_minutes = sum(task.total_minutes for task in tasks)
        estimated_hours = max(1, round(total_minutes / 60))
        
        return {
            "plan": "\n".join(plan_parts),
            "estimated_hours": estimated_hours,
            "note": "Generated using local logic (AI service unavailable)"
        }

    # Then update the _get_fallback_response method:
    def _get_fallback_response(self, user=None):
        """Return a fallback response when AI service is unavailable"""
        if user:
            # Try to generate a local plan if we have user context
            return Response(self._generate_local_plan(user))
        
        # Generic fallback
        fallback_response = {
            "plan": "Complete all tasks in order of priority. Focus on in-progress items first. Start with the most time-sensitive tasks.",
            "estimated_hours": 4,
            "note": "AI service is currently unavailable. This is a default plan."
        }
        return Response(fallback_response)