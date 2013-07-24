from django.contrib import admin

from .models import *

admin.site.register([
    Cluster,
    Block,
    EducationDistrict,
    Village,
    State
])
