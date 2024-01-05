""" Importations effectue pour la réalisation de la création des vues pour les endpoints """
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from shop.permissions import IsAdminAuthenticated
from shop.serializers import CategoryDetailSerializer
from shop.serializers import CategoryListSerializer
from shop.serializers import ProductListSerializer
from shop.serializers import ProductDetailSerializer
from shop.serializers import ArticleSerializer
from shop.models import Category
from shop.models import Product
from shop.models import Article

"""Création des vues pour les endpoints """
class CategoryViewset(ReadOnlyModelViewSet):
    
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()
    
    
    def get_queryset(self):
        return Category.objects.filter(active=True)
    #Cette methode determine le serializer à retouner et par defaut renvoie le serializer de classe serializer_class 
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
    
    
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()
        

    
class ProductViewset(ReadOnlyModelViewSet):
    
    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    
    
    def get_queryset(self):
        queryset =  Product.objects.filter(active = True)
        category_id = self.request.GET.get('category_id')
        
        if category_id :
            queryset = queryset.filter(category_id = category_id)
        return queryset  
    #Cette methode determine le serializer à retouner et par defaut renvoie le serializer de classe serializer_class 
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
        
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()

    
class ArticleViewset(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    
    def get_queryset(self):
        queryset =  Article.objects.filter(active = True)
        product_id = self.request.GET.get('product_id')
        
        if product_id :
            queryset = queryset.filter(product_id = product_id)
        return queryset  
    

class MultipleSerializerMixin:
    detail_serializer_class = None
    
    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is None:
            return detail_serializer_class
        return super().get_serializer_class()

class AdminCategoryViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()
    #Application d'une permission sur le viewsets
    permission_classes = [IsAdminAuthenticated]
    
class AdminArticleViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class =  ArticleSerializer
    queryset = Article.objects.all()
    
    