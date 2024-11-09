from rest_framework import serializers

from prj_terminology.models import ReferenceElement


class ReferenceElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceElement
        fields = ('code', 'value')
