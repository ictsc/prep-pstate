from django.db import models


class TemplateModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Problem(TemplateModel):
    name = models.CharField("問題名(管理用)", max_length=200)
    display_name = models.CharField("問題名(参加者向け)", max_length=200)
    description = models.TextField("問題文")
    start_date = models.DateTimeField("問題公開日時", blank=True, null=True)
    end_date = models.DateTimeField("問題公開終了日時", blank=True, null=True)
    is_enabled = models.BooleanField("公開フラグ", default=False)
    #   TODO    :   terraform-managerのコードをpstateに持ってきたら下のコメントアウトを外す.
    # terraform_file_id = models.ForeignKey('TerraformFile')
