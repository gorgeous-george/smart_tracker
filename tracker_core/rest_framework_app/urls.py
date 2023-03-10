from django.urls import include, path
from rest_framework import routers
from rest_framework_app import views

router = routers.DefaultRouter()
router.register(r'users', views.ReadOnlyUserViewSet)
router.register(r'datasets', views.DatasetViewSet)
router.register(r'objects', views.CoreObjectViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework_app'))
]