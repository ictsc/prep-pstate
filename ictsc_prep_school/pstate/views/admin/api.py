from rest_framework import viewsets, mixins
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission

from pstate.models import ProblemEnvironment
from pstate.serializers import ProblemEnvironmentSerializer


class IsStaff(BasePermission):
    """
    Allows access only to authenticated and staff users.
    """

    def has_permission(self, request, view):
        return request.user.is_staff and request.user.is_authenticated


class ProblemEnvironmentViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):

    authentication_classes = (BasicAuthentication, )
    permission_classes = (IsAuthenticated, IsStaff)
    queryset = ProblemEnvironment.objects.none()
    serializer_class = ProblemEnvironmentSerializer

    def get_queryset(self):
        return ProblemEnvironment.objects.filter(is_enabled=True)
