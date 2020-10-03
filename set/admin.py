from django.contrib import admin
from .models import Module, Set, Question, Response, AttemptedSet


admin.site.register(Module)
admin.site.register(Set)
admin.site.register(Question)
admin.site.register(Response)
admin.site.register(AttemptedSet)
