from django.contrib import admin
from . import models

for name in dir(models):
    obj = getattr(models, name)
    if type(obj).__name__ == "ModelBase":
        admin.site.register(obj)
