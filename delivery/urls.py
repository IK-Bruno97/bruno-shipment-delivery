from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name="home"),
    path('shipment/', ShipmentView.as_view(), name='shipment'),
    path('track-shipment/', TrackingView.as_view(), name='track-shipment'),
]
