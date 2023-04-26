from rest_framework import viewsets, status, generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item, Category, Order
from .serializers import ItemSerializer, CategorySerializer, OrderSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ItemListCreateAPIView(APIView):
    def get(self, request, category_id, *args, **kwargs):
        items = Item.objects.filter(category_id=category_id)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemRetrieveUpdateDestroyAPIView(APIView):

    def get_item(self, item_id):
        return generics.get_object_or_404(Item, id=item_id)

    def get(self, request, item_id, *args, **kwargs):
        serializer = ItemSerializer(self.get_item(item_id))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, item_id, *args, **kwargs):
        serializer = ItemSerializer(self.get_item(item_id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id, *args, **kwargs):
        self.get_item(item_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderListCreateAPIView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, item_id, *args, **kwargs):
        return self.list(request, item_id, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(item_id=self.kwargs['item_id'])


class OrderRetrieveUpdateDestroyAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_order(self, order_id):
        return generics.get_object_or_404(Order, id=order_id)

    def get(self, request, order_id, *args, **kwargs):
        serializer = OrderSerializer(self.get_order(order_id))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, order_id, *args, **kwargs):
        serializer = OrderSerializer(self.get_order(order_id), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id, *args, **kwargs):
        self.get_order(order_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
