from rest_framework.routers import SimpleRouter
from .views import AnimeAPIView, GenreAPIView


router = SimpleRouter()
router.register("anime", AnimeAPIView)
router.register("genres", GenreAPIView)

urlpatterns = [] + router.urls
