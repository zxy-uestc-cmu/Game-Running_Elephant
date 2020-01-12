from django.urls import path

from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('begin/', views.begin, name='begin'),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('scoreboard/', views.handle_scoreboard, name='scoreboard'),
    path('profile/', views.profile,name='profile'),
    path('personal_edit/', views.personal_edit,name='personal_edit'),
    path('thoughts/', views.thoughts_add, name="thoughts_add"),
    path('thoughts_delete/<thought_id>', views.thoughts_delete, name="thoughts_delete"),
    path('gameover/', views.game_over, name='gameover'),
    path('addfriends/', views.add_friends, name='addfriends'),
    path('friend_profile/<friend_id>', views.friend_profile, name='friend_profile'),
    path('friend_accept/<int:friend_request_id>', views.friend_accept, name='friend_accept'),
    path('friend_reject/<int:friend_request_id>', views.friend_reject, name='friend_reject'),
    path('friend_add/<friend_id>', views.friend_add, name='friend_add'),
    path('friend_delete/<friend_id>', views.friend_delete, name='friend_delete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)