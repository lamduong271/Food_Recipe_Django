from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


from core.models import Tag, Ingredient, Recipe
from recipe import serializers

class BaseRecipeAttrViewSet(viewsets.GenericViewSet, 
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    """Base viewset for owned recipe attribute"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        """return objects for current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)
    

class TagViewSet(BaseRecipeAttrViewSet):
    # """ Manage tags in the database"""
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    # def get_queryset(self):
    #     """return objects for current authenticated user only"""
    #     return self.queryset.filter(user=self.request.user).order_by('-name')
    # def perform_create(self, serializer):
    #     """Create a new tag"""
    #     serializer.save(user=self.request.user)
# Create your views here.

class IngredientViewSet(BaseRecipeAttrViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    # def get_queryset(self):
    #     """return objects for current authenticated user only"""
    #     return self.queryset.filter(user=self.request.user).order_by('-name')
    # def perform_create(self, serializer):
    #     """Create a new ingredient"""
    #     serializer.save(user=self.request.user)

class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        return self.queryset.filter(user=self.request.user)
    def get_serializer_class(self):
        """Return approproate serialier class"""
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        return self.serializer_class
    def perform_create(self,serializer):
        """Create a new recpie"""
        serializer.save(user=self.request.user)
    
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )