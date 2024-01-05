from rest_framework.serializers import ModelSerializer  
from rest_framework import serializers
from shop.models import Category
from shop.models import Product 
from shop.models import Article

""" Création des Serializers ( La sérialisation est le procédé par lequel une hiérarchie d'objets Python est convertie en flux d'octets) Nous avons fait pour les category et les produits  """

class ArticleSerializer(ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'date_created', 'date_updated', 'name', 'price', 'product']
    
    def validate_price(self,value):
        if value<1:
            raise serializers.ValidationError('Price must be greater than 1euro')
        return value
    
    def validate_product(self, value):
        if value.active is False:
            raise serializers.ValidationError('Product must be active')
        return value


class ProductListSerializer(ModelSerializer):
     class Meta:
         model = Product
         fields =  ['id', 'date_created','date_updated', 'name','ecoscore']
        

class ProductDetailSerializer(ModelSerializer):
    articles = ArticleSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id','name','date_created','date_updated','category','articles']
        
    def get_articles(self, instance):
        queryset = instance.article.filter(active=True)
        serilizer  =  ArticleSerializer(queryset, many=True)
        return serilizer.data
    
       
class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'date_created','date_updated', 'name','description']
        
    #Le validate_name permet de faire un contrôle sur  le champs  de validation name il prend value qui va contenir tous les noms . Le validationerror prend en charge l'affichage des messages d'erreurs
    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError('Category already exists')
        return value
    #Le validate permet de faire un contrôle sur tout les champs de validation il prend data qui va contenir toutes les données . Le validationerror prend en charge l'affichage des messages d'erreurs
    
    
    def validate(self, data):
        if data['name'] not in data['description']:
            raise serializers.ValidationError('Name must be in the description')
        return data


class CategoryDetailSerializer(ModelSerializer):
    
    # Nous redéfinissons l'attribut 'product' qui porte le même nom que dans la liste des champs à afficher
    # en lui précisant un serializer paramétré à 'many=True' car les produits sont multiples pour une catégorie
    products = ProductListSerializer(many=True)
    
    class Meta:
        model = Category
        fields = ['id','date_created','date_updated','name','products']
    
    def get_products(self, instance):
        # Le paramètre 'instance' est l'instance de la catégorie consultée.
        # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
        # d'entités dans la liste

        # On applique le filtre sur notre queryset pour n'avoir que les produits actifs
        queryset = instance.products.filter(active=True)
         # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serilizer = ProductSerializer(queryset, many=True)
        # la propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serilizer.data
    

