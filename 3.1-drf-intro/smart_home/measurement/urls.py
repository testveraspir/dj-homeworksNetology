from django.urls import path

from measurement.views import SensorAPIList, SensorAPIUpdate, MeasurementAPIList

urlpatterns = [
    path('sensors/', SensorAPIList.as_view()),
    path('sensors/<int:pk>/', SensorAPIUpdate.as_view()),
    path('measurements/', MeasurementAPIList.as_view()),
]
