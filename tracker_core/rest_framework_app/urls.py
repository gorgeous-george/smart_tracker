from django.urls import include, path
from rest_framework import routers
from rest_framework_app import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router = routers.DefaultRouter()
router.register(r'users', views.ReadOnlyUserViewSet)
router.register(r'datasets', views.DatasetViewSet)
router.register(r'objects', views.CoreObjectViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # django rest framework
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework_app')),
    # drf-spectacular
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
