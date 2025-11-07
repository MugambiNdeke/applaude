from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from projects.views import ProjectViewSet, TestRunViewSet
from billing.views import PaystackWebhookView, PlanList, CreateCheckoutView
from contact.views import ContactSubmitView

# Set up DRF Router
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'runs', TestRunViewSet, basename='testrun')


urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Public Paystack Webhook - Must be outside /api/v1/ for Paystack to access
    path('api/paystack-webhook/', PaystackWebhookView.as_view(), name='paystack-webhook'),

    # API Version 1
    path('api/v1/', include([
        # Djoser Authentication (Login, Logout, User Create, Token Refresh)
        path('auth/', include('djoser.urls')),
        path('auth/', include('djoser.urls.jwt')), # Simple JWT endpoints

        # Billing and Payments
        path('billing/plans/', PlanList.as_view(), name='billing-plans'),
        path('billing/create-checkout/', CreateCheckoutView.as_view(), name='billing-checkout'),

        # Contact Form
        path('contact/submit/', ContactSubmitView.as_view(), name='contact-submit'),

        # Projects and Runs (DRF Viewsets)
        path('', include(router.urls)), 
    ])),
]
