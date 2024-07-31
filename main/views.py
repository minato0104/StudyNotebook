from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import StudyGroup, StudyGoal, StudyHistory
from django.utils.dateparse import parse_date, parse_datetime
import uuid

@login_required
def dashboard_view(request):
    return render(request, 'main/dashboard.html', {'user': request.user})

@login_required
def study_group_view(request):
    groups = StudyGroup.objects.filter(members=request.user)
    return render(request, 'main/study_group.html', {'groups': groups})

@login_required
def create_group_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        study_topic = request.POST.get('study_topic')
        study_duration = int(request.POST.get('study_duration'))
        
        room_number = uuid.uuid4().hex[:8]  # Generate a unique 8-character room number
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(minutes=study_duration)

        group = StudyGroup.objects.create(
            name=name,
            description=description,
            owner=request.user,
            study_topic=study_topic,
            study_time=start_time,
            room_number=room_number,
            end_time=end_time
        )
        group.members.add(request.user)
        return redirect('study_group_detail', group_id=group.id)

    return render(request, 'main/create_group.html')

@login_required
def study_group_detail_view(request, group_id):
    group = get_object_or_404(StudyGroup, id=group_id)
    current_time = timezone.now()
    
    if current_time >= group.end_time and not group.is_completed:
        group.is_completed = True
        group.save()
        
        StudyHistory.objects.create(
            user=request.user,
            group_name=group.name,
            completed_on=group.end_time,
            details=f"Studied {group.study_topic} for {(group.end_time - group.study_time).total_seconds() / 60} minutes"
        )
    
    context = {
        'group': group,
        'is_completed': group.is_completed,
        'remaining_time': (group.end_time - current_time).total_seconds() if current_time < group.end_time else 0
    }
    return render(request, 'main/study_group_detail.html', context)

@login_required
def join_group_view(request):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        try:
            group = StudyGroup.objects.get(room_number=room_number)
            group.members.add(request.user)
            return redirect('study_group_detail', group_id=group.id)
        except StudyGroup.DoesNotExist:
            return render(request, 'main/join_group.html', {'error': '房间号不存在，请检查后重试。'})

    return render(request, 'main/join_group.html')

@login_required
def study_goals_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            goal_text = request.POST.get('goal')
            begin_date_str = request.POST.get('begin_date')
            target_date_str = request.POST.get('target_date')

            begin_date = parse_date(begin_date_str) if begin_date_str else None
            target_date = parse_date(target_date_str) if target_date_str else None

            if not goal_text or not begin_date or not target_date:
                return render(request, 'main/study_goals.html', {
                    'goals': StudyGoal.objects.filter(user=request.user),
                    'error': '所有字段都是必填项，请确保填写正确。'
                })

            StudyGoal.objects.create(
                user=request.user,
                goal=goal_text,
                begin_date=begin_date,
                target_date=target_date,
                completed=False
            )
        
        elif action == 'complete':
            goal_id = request.POST.get('goal_id')
            goal = get_object_or_404(StudyGoal, id=goal_id, user=request.user)
            
            if not goal.completed:
                goal.completed = True
                goal.save()

                StudyHistory.objects.create(
                    user=request.user,
                    goal=goal,
                    completed_on=timezone.now(),
                    details=f"Goal '{goal.goal}' completed."
                )

    goals = StudyGoal.objects.filter(user=request.user)
    return render(request, 'main/study_goals.html', {'goals': goals})

@login_required
def study_history_view(request):
    history = StudyHistory.objects.filter(user=request.user).order_by('-completed_on')
    return render(request, 'main/study_history.html', {'history': history})
