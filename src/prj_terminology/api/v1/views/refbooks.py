from datetime import datetime

from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from prj_terminology.api.v1.serializers.refbooks import *

from prj_terminology.models import *


@extend_schema(
    tags=['Refbooks'],
    parameters=[
        OpenApiParameter(
            name='date',
            type=OpenApiTypes.DATE,
            location=OpenApiParameter.QUERY,
            description='Дата начала действия в формате ГГГГ-ММ-ДД',
            required=False,
        ),
    ],
)
class ReferenceListAPIView(APIView):
    serializer_class = RefBooksSerializer

    def get_queryset(self):
        qs = Reference.objects.all()
        date = self.request.query_params.get('date')
        if date is not None:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            qs = qs.filter(versions__start_date__lte=date).distinct()
        return qs

    def get(self, request):
        return Response({
            'refbooks': ReferenceSerializer(
                self.get_queryset(), many=True).data
        })


@extend_schema(
    tags=['Refbooks'],
    parameters=[
        OpenApiParameter(
            name='id',
            location=OpenApiParameter.PATH,
            type=OpenApiTypes.INT,
            description='Идентификатор справочника',
        ),
        OpenApiParameter(
            name='version',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Версия справочника',
            required=False,
        ),
    ],
)
class ReferenceRetrieveAPIView(RetrieveAPIView):
    serializer_class = ReferenceSerializerVersionSerializer

    def get_object(self):
        qs = (
            ReferenceVersion.objects
            .filter(reference_id=int(self.kwargs['pk']))
        )
        version = self.request.query_params.get('version')
        if version is not None:
            instance = qs.filter(code=version).first()
        else:
            instance = qs.active_version()
        if instance is None:
            raise NotFound
        return instance


@extend_schema(
    tags=['Refbooks'],
    parameters=[
        OpenApiParameter(
            name='id',
            location=OpenApiParameter.PATH,
            type=OpenApiTypes.INT,
            description='Идентификатор справочника',
        ),
        OpenApiParameter(
            name='code',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Код элемента справочника',
            required=True,
        ),
        OpenApiParameter(
            name='value',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Значение элемента справочника',
            required=True,
        ),
        OpenApiParameter(
            name='version',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Версия справочника',
            required=False,
        ),
    ],
)
class ValidateElementAPIView(APIView):
    def get(self, request, pk):
        version = self.request.query_params.get('version')
        if version is not None:
            qs = ReferenceVersion.objects.get(
                reference_id=pk,
                code=version,
            ).elements.all()
        else:
            instance = (
                ReferenceVersion.objects
                .filter(reference_id=pk)
                .active_version()
            )
            if instance is None:
                raise NotFound
            qs = instance.elements.all()
        return Response(qs.filter(
            code=self.request.query_params['code'],
            value=self.request.query_params['value'],
        ).exists())
