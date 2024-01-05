from django.urls import reverse_lazy,reverse
from rest_framework.test import APITestCase
from unittest import mock
from shop.models import Category,Product
from shop.mocks import  mock_openfoodfact_success, ECOSCORE_GRADE

class ShopApiTestCase(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Fruits', active=True)
        Category.objects.create(name='Légume', active=False)
        
        cls.product = cls.category.products.create(name='Ana')
        cls.category.products.create()
        
    
    def get_product_detail_data(self,product):
        return {
            'id': product.pk,
            'name': product.name,
            'date_created':product.date_created,
            'date_updated':product.date_updated,
            'category':product.category_id,
            'articles': self.get_article_detail_data(product.articles.filter(active=True)),
            'ecoscore': ECOSCORE_GRADE  # la valeur de l'ecoscore provient de notre constante utilisée dans notre mock
            
            
        }
        
    
    



class TestCategory(APITestCase):
     # Nous stockons l’url de l'endpoint dans un attribut de classe pour pouvoir l’utiliser plus facilement dans chacun de nos tests
    url = reverse_lazy('category-list')
    
    def format_datetime(self,value):
         # Cette méthode est un helper permettant de formater une date en chaine de caractères sous le même format que celui de l’api
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    def test_list(self):
        #création de deux catégories dont une seule est active
        category = Category.objects.create(name="Exotics", active=True)
        Category.objects.create(name="Légumes", active=False)
        
    
        # On réalise l’appel en GET en utilisant le client de la classe de test
        response = self.client.get(self.url)
        # Nous vérifions que le status code est bien 200
        # et que les valeurs retournées sont bien celles attendues
        self.assertEqual(response.status_code, 200)
        
        exepted = [
            {
                "id": category.pk,
                "name": category.name,
                "date_created": self.format_datetime(category.date_created),
                "date_updated": self.format_datetime(category.date_updated),
            }
        ]

        self.assertEqual(response.json() , exepted)
    
    def test_create(self):
         # Nous vérifions qu’aucune catégorie n'existe avant de tenter d’en créer une
        self.assertFalse(Category.objects.exists())
        response = self.client.post(self.url, data={"name":"tentative"})
         # Vérifions que le status code est bien en erreur et nous empêche de créer une catégorie
        self.assertEqual(response.status_code, 405)
        # Enfin, vérifions qu'aucune nouvelle catégorie n’a été créée malgré le status code 405
        self.assertFalse(Category.objects.exists())



class TestProduct(ShopApiTestCase):
    @mock.patch('shop.models.Product.call_external_api', mock_openfoodfact_success)
    # Le premier paramètre est la méthode à mocker
    # Le second est le mock à appliquer
    def testdetail(self):
        response = self.client.get(reverse('product_détail', kwargs={'pk':self.product.pk}))
        self.assertEqual(response.status_code,200)
        self.assertEqual(self.get_product_detail_data(self.product), response.json())
        