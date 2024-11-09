from django.urls import path

from prj_terminology.api.v1.views import refbooks

urlpatterns = [
    path(
        'refbooks',
        refbooks.ReferenceListAPIView.as_view(),
    ),
    path(
        'refbooks/<int:pk>/elements',
        refbooks.ReferenceRetrieveAPIView.as_view(),
    ),
    path(
        'refbooks/<int:pk>/check_element',
        refbooks.ValidateElementAPIView.as_view(),
    )
]
