from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorListSerializer, SensorDetailSerializer, MeasurementSerializer


class SensorAPIList(ListCreateAPIView):
    """
    Создание датчика или получение списка датчиков.
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorListSerializer


class SensorAPIUpdate(RetrieveUpdateAPIView):
    """
    Изменение датчика или получение информации по конкретному датчику.
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class MeasurementAPIList(CreateAPIView):
    """
    Добавление измерение. Указываются ID датчика и температура.
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def perform_create(self, serializer):
        try:
            sensor_id = self.request.data.get('sensor')
            sensor = Sensor.objects.get(pk=sensor_id)
            serializer.save(sensor=sensor)
        except Sensor.DoesNotExist:
            raise ValidationError(f"Датчика с id = {sensor_id} не существует.")
