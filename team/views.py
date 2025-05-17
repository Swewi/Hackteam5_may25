from django.shortcuts import render
from .models import TeamMember

def team(request):
    team_members = TeamMember.objects.filter(is_active=True).order_by('-display_order', 'name')
    context = {
        'team_members': team_members,
        'page_title': 'Our Team',
    }
    return render(request, 'team/team.html', context)
