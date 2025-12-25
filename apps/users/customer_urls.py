from django.urls import path

from .views import CustomerInquiryListCreateView

urlpatterns = [
    path('inqury/', CustomerInquiryListCreateView.as_view(), name='customer_inqury'),
]
