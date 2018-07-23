from rest_framework import serializers

from pstate.models import ProblemEnvironment


class ProblemEnvironmentSerializer(serializers.ModelSerializer):
    terraform_state = serializers.SerializerMethodField()
    problem = serializers.StringRelatedField()
    team = serializers.StringRelatedField()

    class Meta:
        model = ProblemEnvironment
        fields = ('id',
                  'vnc_server_ipv4_address',
                  'vnc_server_password',
                  'state',
                  'terraform_state',
                  'problem',
                  'team'
                  )

    def get_terraform_state(self, obj):
        return obj.environment.state
