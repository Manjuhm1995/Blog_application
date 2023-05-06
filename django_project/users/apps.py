from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
#     to avoid import sideeffects we need to create method that is the following method
    def ready(self):
        import users.signals
