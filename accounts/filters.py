import django_filters
from django_filters import DateFilter, CharFilter
from django_filters.widgets import RangeWidget
from .models import *
from django import forms


class OrderFilter(django_filters.FilterSet):
    created_min = DateFilter(field_name='date_created', lookup_expr='gte', label='Date is greater than or equal to')
    created_max = DateFilter(field_name='date_created', lookup_expr='lte',  label='Date is less than or equal to')


    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created', 'note']


class MenuFilter(django_filters.FilterSet):
    name_filter = CharFilter(field_name='name', lookup_expr='icontains')


    class Meta:
        model = Menu
        fields = '__all__'
        exclude = ['description', 'price', 'image', 'date_created', 'name']



