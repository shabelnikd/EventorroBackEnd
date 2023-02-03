from rest_framework import serializers
from category.models import Category

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )

class CategoryListSerializer(serializers.ModelSerializer):
    # children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('name', )


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['sub'] = SubCategorySerializer(instance.children.all(), many=True).data
        return rep

