from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.core.cache import CacheMixin
from api.v1.notes.serializers import NoteSerializer
from api.core.pagination import CustomPagination
from api.v1.notes.models import Note
from api.v1.users.permissions import IsOwner

class NoteViewSet(viewsets.ModelViewSet,
                  CacheMixin):
    serializer_class = NoteSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    queryset = Note.objects.select_related('user')

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsOwner()]
        elif self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action in ['create']:
            return [IsAuthenticated()]
        else:
            return super().get_permissions()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        data = self.get_cached_data(
            request=request,
            prefix='notes',
            queryset=queryset,
            page=page,
            serializer_class=self.get_serializer,
            paginated_response=self.get_paginated_response
        )
        return Response(data)

def index(request):
    return render(request, 'index.html')