from django.urls import include, path

from .views import delete_user, load_user, save_user

user_patterns = [
    path('save/', save_user, name='save-user'),
    path('load/<int:user_id>', load_user, name='load-user'),
    path('remove/<int:user_id>', delete_user, name='delete-user'),
]

urlpatterns = [
    path('user/', include(user_patterns)),
]