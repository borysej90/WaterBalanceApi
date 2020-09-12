from django.urls import include, path

from .views import delete_user, load_all_users, load_user, save_user

user_patterns = [
    path('load/all', load_all_users, name='load-all-users'),
    path('load/<int:user_id>', load_user, name='load-user'),
    path('save/<int:user_id>', save_user, name='save-user'),
    path('remove/<int:user_id>', delete_user, name='delete-user'),
]

urlpatterns = [
    path('user/', include(user_patterns)),
]