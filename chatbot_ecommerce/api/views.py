from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Product
from core.serializers import ProductSerializer  # You'll create this next

@api_view(['GET'])
def top_products(request):
    products = Product.objects.order_by('-stock')[:3]  # Get top 3 products by stock (descending)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
