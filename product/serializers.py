from rest_framework import serializers

from product.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ('created_at', 'updated_at')

        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False},
            'article': {'required': True, 'allow_blank': False},
            'category': {'required': True},
            'firm': {'required': True, 'allow_blank': False},
            'price': {'required': True},
            'amount': {'required': True},
        }
