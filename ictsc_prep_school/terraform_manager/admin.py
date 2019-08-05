from django.contrib import admin

from terraform_manager.models import Log, Variable, Environment, TerraformFile, ShellScript, Provider, Attribute, \
    FileTemplate

admin.site.register(Log)
admin.site.register(Variable)
admin.site.register(Environment)
admin.site.register(TerraformFile)
admin.site.register(ShellScript)
admin.site.register(Provider)
admin.site.register(Attribute)
admin.site.register(FileTemplate)
