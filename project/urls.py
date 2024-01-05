""" Création d'urls pour acceder aux données """
from rest_framework import routers
from django.contrib import admin
from django.urls import path, include

from shop.views import CategoryViewset
from shop.views import ProductViewset
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from shop.views import ArticleViewset,AdminCategoryViewset,AdminArticleViewset


router  = routers.SimpleRouter()
router.register('category',CategoryViewset, basename='category')
router.register('product',ProductViewset, basename='product')
router.register('article',ArticleViewset, basename='article')
router.register('admin/category',AdminCategoryViewset, basename='admin-category' )
router.register('admin/article', AdminArticleViewset, basename='admin-article')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls))
]
