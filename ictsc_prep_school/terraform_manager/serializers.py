from rest_framework import serializers
from terraform_manager.models import TerraformFile, Environment


class TerraformFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerraformFile
        fields = ('id', 'name', 'body', 'created_at', 'updated_at',)


class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = ('id', 'terraform_file',)
        read_only_fields = ('id', 'created_at', 'updated_at',)

    def create(self, validated_data):
        environment = Environment.objects.create(**validated_data)
        return environment
