from django.urls import path

from .views import CustomerInquiryListCreateView, CustomerInquiryContactUpdateView

urlpatterns = [
    path('inqury/', CustomerInquiryListCreateView.as_view(), name='customer_inqury'),
    path('inqury/<int:pk>/contacted/', CustomerInquiryContactUpdateView.as_view(), name='customer_inqury_contacted'),
]
