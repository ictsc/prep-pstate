from rest_framework import viewsets, mixins
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response

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

    @list_route(methods=['post'], url_path='bulk')
    def get_problem_environment(self, request, *args, **kwargs):
        try:
            qs = self.get_queryset()
            id_list = request.data.get("id")
            if id_list:
                qs = qs.filter(id__in=id_list)
            serializer = self.get_serializer(data=qs, many=True)
            serializer.is_valid()
        except:
            return Response([])
        return Response(serializer.data)
