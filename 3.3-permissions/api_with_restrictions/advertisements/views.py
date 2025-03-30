from django.forms import model_to_dict
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, FavoriteAdvertisement
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""

        if self.action == "create":
            return [IsAuthenticated()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []

    @action(detail=True, methods=["post", "delete"])
    def favorite(self, request, pk=None):
        """Добавление или удаление избранного объявления."""

        if not request.user.is_authenticated:
            return Response({"error": "Вы должны быть авторизованы,"
                                      " чтобы добавлять объявления в избранное."})

        advertisement = self.get_object()
        if advertisement.creator == request.user:
            return Response({"error": "Нельзя добавлять в избранное"
                                      " собственные объявления."})

        if request.method == "POST":
            favorite, created = FavoriteAdvertisement.objects.get_or_create(user=request.user,
                                                                        advertisement=advertisement)

            if created:
                return Response({"message": "Объявление добавлено в избранное",
                                 "advertisement": model_to_dict(favorite)})
            else:
                return Response({"error": "Объявление уже есть в избранных."})

        if request.method == "DELETE":
            try:
                favorite = FavoriteAdvertisement.objects.get(user=request.user,
                                                             advertisement=advertisement)
                favorite.delete()
                return Response({"message": "Объявление успешно удалено из избранных."})
            except FavoriteAdvertisement.DoesNotExist:
                return Response({"error": "Объявление в избранных нет."})
        return Response({"error": "Что-то пошло не так."})
