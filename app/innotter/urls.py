from rest_framework.routers import DefaultRouter

from innotter import views

router = DefaultRouter()
router.register(r"page", views.PageViewSet)
router.register(r"post", views.PostViewSet)
router.register(r"feed", views.FeedViewSet, basename="feed")
router.register(r"tag", views.TagViewSet)
router.register(r"tags", views.TagsViewSet)

urlpatterns = router.urls
