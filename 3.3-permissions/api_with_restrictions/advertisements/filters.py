from django_filters import rest_framework as filters, DateFromToRangeFilter
from django_filters.rest_framework import BooleanFilter

from advertisements.models import Advertisement, FavoriteAdvertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    created_at = DateFromToRangeFilter()
    is_favorite = BooleanFilter(method='filter_is_favorite')

    def filter_is_favorite(self, queryset, name, value):
        user = self.request.user

        if user.is_authenticated:
            favorite_id = FavoriteAdvertisement.objects.filter(user=user). \
                values_list("advertisement__id", flat=True)
            # если is_favorite=True
            if value:
                return queryset.filter(id__in=favorite_id)
            # если is_favorite=False
            else:
                return queryset.exclude(id__in=favorite_id)
        return queryset

    class Meta:
        model = Advertisement
        fields = ["status", "created_at", "creator"]
