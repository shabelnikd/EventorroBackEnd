from rest_framework import serializers
from category.models import Category

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('parent', )

class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('parent', )


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        subcategory = SubCategorySerializer(instance.children.all(), many=True).data
        if subcategory != []:
            rep['sub'] = subcategory
        return rep
