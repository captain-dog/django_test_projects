from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.QuestionModelViewSet, basename="kek")

urlpatterns = router.urls
