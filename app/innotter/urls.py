from rest_framework.routers import DefaultRouter

from innotter import views

router = DefaultRouter()
router.register(r'pages', views.PageViewSet)
router.register(r'posts', views.PostViewSet)

urlpatterns = router.urls