from rest_framework import viewsets, status
from rest_framework import routers
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from terraform_manager.models import TerraformFile, Environment
from terraform_manager.serializers import EnvironmentSerializer, TerraformFileSerializer


class TerraformFileViewSet(viewsets.ModelViewSet):
    queryset = TerraformFile.objects.all()
    serializer_class = TerraformFileSerializer

    @detail_route(methods=['post'])
    def create_environment(self, *args, **kwargs):
        from terraform_manager.serializers import EnvironmentSerializer
        data = {"terraform_file": kwargs['pk'], 'state': 'none'}
        serializer = EnvironmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            from terraform_manager.terraform_manager_tasks import copy_tf_files
            copy_tf_files.delay(serializer.instance.id, serializer.validated_data['terraform_file'].id)
            return Response(serializer.data)
        else:
            return Response(serializer.error_messages)

    @detail_route(methods=['post'])
    def direct_apply(self, *args, **kwargs):
        from terraform_manager.serializers import EnvironmentSerializer
        data = {"terraform_file": kwargs['pk'], 'state': 'none'}
        serializer = EnvironmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            from terraform_manager.terraform_manager_tasks import direct_apply
            var = self.request.data['var']
            direct_apply.delay(serializer.instance.id, serializer.validated_data['terraform_file'].id, var)
            return Response(serializer.data)
        else:
            return Response(serializer.error_messages)


class EnvironmentViewSet(viewsets.ModelViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer

    @detail_route(methods=['put'])
    def init(self, *args, **kwargs):
        from terraform_manager.terraform_manager_tasks import init
        if self.get_object().is_locked:
            return Response(status=status.HTTP_409_CONFLICT)
        else:
            init.delay(self.get_object().id)
            return Response()

    @detail_route(methods=['put'])
    def plan(self, *args, **kwargs):
        from terraform_manager.terraform_manager_tasks import plan
        if self.get_object().is_locked:
            return Response(status=status.HTTP_409_CONFLICT)
        else:
            var = self.request.data['var']
            plan.delay(self.get_object().id, var)
            return Response()

    @detail_route(methods=['put'])
    def apply(self, *args, **kwargs):
        from terraform_manager.terraform_manager_tasks import apply
        if self.get_object().is_locked:
            return Response(status=status.HTTP_409_CONFLICT)
        else:
            var = self.request.data['var']
            apply.delay(self.get_object().id, var)
            return Response()

    @detail_route(methods=['put'], url_path='destroy')
    def _destroy(self, *args, **kwargs):
        from terraform_manager.terraform_manager_tasks import destroy
        if self.get_object().is_locked:
            return Response(status=status.HTTP_409_CONFLICT)
        else:
            var = self.request.data['var']
            destroy.delay(self.get_object().id, var)
            return Response()


class CeleryExampleViewSet(viewsets.ViewSet):
    def list(self, request):
        from terraform_manager.terraform_manager_tasks import debug_task
        debug_task.delay()
        return Response()


router = routers.SimpleRouter()
router.register(r'terraform_files', TerraformFileViewSet)
router.register(r'celery_example', CeleryExampleViewSet, base_name="celery-example")
router.register(r'environments', EnvironmentViewSet, base_name="environments")
# router.register(r'accounts', AccountViewSet)
urlpatterns = router.urls
