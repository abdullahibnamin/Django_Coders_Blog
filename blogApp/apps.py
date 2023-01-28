from django.apps import AppConfig


class BlogappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blogApp'

    # def ready(self) -> None:
    #     from .scheduler import scheduler
    #     scheduler.start()
