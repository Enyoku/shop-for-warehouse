from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from product.models import Category, Product
from product.filters import ProductFilter
from product.serializers import CategorySerializer, ProductSerializer


# Views for Category

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_new_category(request):
    data = request.data
    category = CategorySerializer(data=data)
    
    if category.is_valid():
            if not Category.objects.filter(name=data['name']).exists():
                category = Category.objects.create(name=data['name'])
                res = CategorySerializer(category, many=False)
                return Response({'category': res.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Category is already exists'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(category.errors)


@api_view(['GET'])
def get_all_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response({'categories': serializer.data}, status=status.HTTP_200_OK)


# Views for Product

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_product(request):
    data = request.data
    print(dict(**data))
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        product = Product.objects.create(
            name=data['name'],
            article=data['article'],
            description=data['description'],
            category=Category.objects.get(id=data['category']),
            firm=data['firm'],
            price=data['price'],
            amount=data['amount']
        )
        return Response({'product': serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_products(request):
    filterset = ProductFilter(
        request.GET, 
        queryset=Product.objects.all().order_by('id')
    )

    count = filterset.qs.count()

    # Pagination
    resPerPage = 6

    paginator = PageNumberPagination()
    paginator.page_size = resPerPage
    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = ProductSerializer(queryset, many=True)
    return Response({
        'resPerPage': resPerPage,
        'count': count,
        'products': serializer.data
    })
