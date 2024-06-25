from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import Product, Order
from .serializers import ProductSerializer, OrderProductSerializer, CreateProductSerializer

@swagger_auto_schema(method='post', request_body=CreateProductSerializer)
@api_view(['POST'])
def create_product(request):
    serializer = CreateProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='patch', request_body=ProductSerializer)
@api_view(['PATCH'])
def update_stock(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post', request_body=OrderProductSerializer)
@api_view(['POST'])
def create_order(request):
    serializer = OrderProductSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()

        order_folio = f"ORD-{order.id}"

        return Response({"folio": order_folio}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)