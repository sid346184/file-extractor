from django.urls import path
from .views import ExtractTextView

urlpatterns = [
    path('extract-text/', ExtractTextView.as_view(), name='extract-text'),
]
