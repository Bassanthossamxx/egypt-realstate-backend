from django.urls import path

from .views import DeveloperListCreateView, DeveloperRetrieveUpdateDestroyView

urlpatterns = [
    path('developers/', DeveloperListCreateView.as_view(), name='developer-list-create'),
    path('developers/<int:pk>/', DeveloperRetrieveUpdateDestroyView.as_view(), name='developer-detail'),
]
