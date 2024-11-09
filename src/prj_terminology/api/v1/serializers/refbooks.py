from rest_framework import serializers

from prj_terminology.models import Reference, ReferenceVersion
from prj_terminology.api.v1.serializers.elements import (
    ReferenceElementSerializer
)


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ('id', 'code', 'name')


class RefBooksSerializer(serializers.Serializer):
    refbooks = ReferenceSerializer(many=True)


class ReferenceSerializerVersionSerializer(serializers.ModelSerializer):
    elements = ReferenceElementSerializer(many=True)

    class Meta:
        model = ReferenceVersion
        fields = ('elements',)
