from django.db.models.aggregates import Avg
from rest_framework import serializers
from taggit.serializers import TagListSerializerField , TaggitSerializer


from .models import Product , Brand , Review


class BrandListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'



class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'



class ProductListSerializers(serializers.ModelSerializer):
    # brand = BrandListSerializers()  # Show all data off brand
    brand = serializers.StringRelatedField()   # show name of brand this product
    avg_rate = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
    
    def get_avg_rate(self, product):
        avg = product.review_product.aggregate(rate_avg=Avg('rate'))
        if not avg['rate_avg']:
            return 0
        return avg['rate_avg']
    
    def get_review_count(self, product:Product):
        review = product.review_product.all().count()
        return review



class ProductDetailSerializers(TaggitSerializer,serializers.ModelSerializer):
    brand = BrandListSerializers()
    avg_rate = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    review = ReviewSerializers(source='review_product',many=True)
    tags = TagListSerializerField() 

    class Meta:
        model = Product
        fields = '__all__'
    
    def get_avg_rate(self, product):
        avg = product.review_product.aggregate(rate_avg=Avg('rate'))
        if not avg['rate_avg']:
            return 0
        return avg['rate_avg']
    
    def get_review_count(self, product:Product):
        review = product.review_product.all().count()
        return review



class BrandDetailSerializers(serializers.ModelSerializer):
    products = ProductListSerializers(source='product_name', many=True)
    class Meta:
        model = Brand
        fields = '__all__'



class ProductCartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','image','price']