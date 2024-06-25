from rest_framework import serializers
from .models import Product, Order, OrderProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['stock', 'price']

class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'stock', 'price']

class OrderProductSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product.id')
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = OrderProduct
        fields = ['product_id', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['products', 'total', 'created_at']

    def validate_products(self, value):
        for product_data in value:
            product_id = product_data['product_id']
            quantity = product_data['quantity']

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"No se encontró producto con ID {product_id}")

            if product.stock < quantity:
                raise serializers.ValidationError(f"Insuficiente stock para el producto con ID {product_id}")

        return value

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order_total = 0

        order = Order.objects.create(total=order_total)

        for product_data in products_data:
            product_id = product_data['product_id']
            quantity = product_data['quantity']

            product = Product.objects.get(id=product_id)

            # Aquí podrías crear o asociar OrderProduct con Order y Product
            OrderProduct.objects.create(order=order, product=product, quantity=quantity)

            order_total += product.price * quantity
        
        order.total = order_total
        order.save()

        return order