from rest_framework import serializers
from EmailApp.models import EmailInfo

class EmailInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=EmailInfo
        fields=('EmailInfoId','EmailInfoUserEmail')