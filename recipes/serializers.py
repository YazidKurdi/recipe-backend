from rest_framework import serializers

from .models import Recipes,Ingredients,Cuisine

class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ingredients model
    """
    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'unit', 'amount')


class CuisineSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cuisine model
    """
    class Meta:
        model = Cuisine
        fields = ('id', 'name', 'image')


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Recipes model
    """
    # Nesting IngredientSerializer within RecipeSerializer
    ingredients = IngredientSerializer(many=True)
    # SerializerMethodField to format the date for the updated_at field
    updated_at = serializers.SerializerMethodField()
    # SlugRelatedField for the cuisine field to get only the name of the related object
    cuisine = serializers.SlugRelatedField(slug_field='name', queryset=Cuisine.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Recipes
        fields = (
            "id",
            "title",
            "description",
            "thumbnail",
            "updated_at",
            "author",
            "ingredients",
            "cuisine",
            "ai_generated"
        )

    def to_representation(self, instance):
        """
        Overriding the to_representation method to handle the thumbnail field
        """
        data = super().to_representation(instance)

        # If the thumbnail field is empty, replace it with the cuisine image
        if not instance.thumbnail:
            cuisine = instance.cuisine
            if cuisine:
                cuisine_data = CuisineSerializer(cuisine).data
                cuisine_image = cuisine_data.get('image')
                if cuisine_image:
                    data['thumbnail'] = cuisine_image

        return data

    def get_updated_at(self, instance):
        """
        Custom method to format the date for the updated_at field
        """
        return instance.updated_at.date().strftime('%d %B %Y')

    def create(self, validated_data):
        """
        Overriding the create method to handle the nested ingredients field
        """
        ingredient_data = validated_data.pop('ingredients')
        recipe = Recipes.objects.create(**validated_data)
        for ingredient in ingredient_data:
            ingredient_name = ingredient.get('name')
            existing_ingredient = Ingredients.objects.filter(name=ingredient_name).first()
            if existing_ingredient:
                recipe.ingredients.add(existing_ingredient)
            else:
                new_ingredient = Ingredients.objects.create(**ingredient)
                recipe.ingredients.add(new_ingredient)
        return recipe

    def update(self, instance, validated_data):
        """
        Overriding the update method to handle the nested ingredients field
        """
        ingredients_data = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id', None)
            if ingredient_id:
                ingredient = instance.ingredients.get(id=ingredient_id)
                IngredientSerializer().update(ingredient, ingredient_data)
            else:
                ingredient = Ingredients.objects.create(**ingredient_data)
                instance.ingredients.add(ingredient)
        return instance

class AllRecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for returning a simplified representation of a recipe,
    including only its title, description, ingredients, and cuisine (if any).
    """

    ingredients = IngredientSerializer(many=True)
    cuisine = serializers.SlugRelatedField(slug_field='name', queryset=Cuisine.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Recipes
        fields = (
            "title",
            "description",
            "ingredients",
            "cuisine"
        )



