from django.apps import AppConfig
from django.db.models.signals import post_migrate

def init_admin(sender, **kwargs):
    from server.models import WebUser
    if not WebUser.objects.exists():
        WebUser.objects.create_user(username='admin', password='admin')


class ServerConfig(AppConfig):
    name = 'server'

    def ready(self):
        post_migrate.connect(init_admin, sender=self)
