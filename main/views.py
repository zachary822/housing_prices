import django_filters.rest_framework as filters
from django.db.models import Avg
from django.db.models.functions import TruncYear
from django.forms import fields, widgets
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.views import Response

from .models import Sale
from .serializers import SaleSerializer, SummarySerializer


class DateInput(widgets.DateInput):
    input_type = "date"


class DateField(fields.DateField):
    widget = DateInput


class DateFilter(filters.DateFilter):
    field_class = DateField


class SaleFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = filters.NumberFilter(field_name="price", lookup_expr='lte')
    date_after = DateFilter(field_name="date", lookup_expr="gte", input_formats=["%Y-%m-%d", "%Y/%m/%d"])
    date_before = DateFilter(field_name="date", lookup_expr="lte", input_formats=["%Y-%m-%d", "%Y/%m/%d"])
    borough = filters.Filter(field_name="neighborhood__borough__name")
    neighborhood = filters.Filter(field_name="neighborhood__name")

    class Meta:
        model = Sale
        fields = []


class SaleSchema(AutoSchema):
    def allows_filters(self, path, method):
        if getattr(self.view, 'filter_backends', None) is None:
            return False
        if hasattr(self.view, 'action'):
            return self.view.action in ["list", "retrieve", "update", "partial_update", "destroy", "summary"]
        return method.lower() in ["get", "put", "patch", "delete"]


class SaleViewSet(viewsets.ModelViewSet):
    schema = SaleSchema()
    queryset = (Sale.objects.all()
                .prefetch_related('neighborhood', 'neighborhood__borough')
                .order_by('pk'))
    serializer_class = SaleSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = SaleFilter

    @action(methods=['get'], detail=False, serializer_class=SummarySerializer)
    def summary(self, request):
        """
        Average price for each year
        """
        queryset = Sale.objects.values('price', 'date').all()
        queryset = (self.filter_queryset(queryset)
                    .annotate(year=TruncYear('date'))
                    .values('year')
                    .annotate(avg=Avg('price'))
                    .order_by('year')
                    .values_list('year', 'avg'))

        return Response({
            'result': ({'year': y.year, 'avg': avg} for y, avg in queryset)
        })


class SaleSummaryView(TemplateView):
    template_name = "main/index.html"
