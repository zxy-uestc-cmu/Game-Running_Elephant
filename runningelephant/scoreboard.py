from .models import Score
from django.http import JsonResponse
from django.shortcuts import render

def refresh():
    records = get_context()
    return JsonResponse({'records':records})


def get_scoreboard(request):
    records = get_context()
    return render(request, 'runningelephant/scoreboard.html', {'records':records})


def get_context():
    scores = Score.objects.all().order_by('-score','-time')[:20]
    records = []
    rank = 1
    for score in scores:
        record = {}
        record['rank'] = rank
        record['player'] = score.player.user.username
        record['score'] = score.score
        record['time'] = score.time
        rank += 1
        records.append(record)
    return records

    


