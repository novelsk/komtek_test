from django.urls import path, include


urlpatterns = [
    path('v1/', include('prj_terminology.api.v1.urls'))
]
