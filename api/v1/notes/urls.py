from rest_framework import  routers
from django.urls import path, include

from api.v1.notes.views import NoteViewSet

router = routers.DefaultRouter()
router.register('notes', NoteViewSet, basename='notes')

urlpatterns = [
    path('', include(router.urls))
]