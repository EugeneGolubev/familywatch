from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from . import models

for name in dir(models):
    obj = getattr(models, name)
    if hasattr(obj, "_meta") and getattr(obj._meta, "app_label", None) == "catalog":
        try:
            admin.site.register(obj)
        except AlreadyRegistered:
            pass
