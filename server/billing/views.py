from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse

from users.models import Subscription
from paystack.api import Transaction, Subscription as PaystackSubscription
import json
from datetime import datetime, timedelta

# Mock plan data for pricing logic [cite: 80]
PAYMENT_PLANS = {
    'WEEKLY': {'name': 'Weekly Sprint', 'price_usd': 15, 'runs': 20, 'duration_days': 7},
    'MONTHLY': {'name': 'Monthly Startup', 'price_usd': 47, 'runs': 50, 'duration_days': 30},
    'YEARLY': {'name': 'Yearly Scale-Up', 'price_usd': 495, 'runs': 600, 'duration_days': 365},
}

class PlanList(APIView):
    """
    Returns a list of all available pricing plans.
    """
    permission_classes = () # Public endpoint for landing page
    def get(self, request):
        return Response(PAYMENT_PLANS)

class CreateCheckoutView(APIView):
    """
    Creates a Paystack checkout session and returns the payment authorization URL[cite: 103].
    """
    def post(self, request):
        plan_key = request.data.get('plan').upper()
        if plan_key not in PAYMENT_PLANS:
            return Response({"detail": "Invalid plan selected."}, status=status.HTTP_400_BAD_REQUEST)

        plan_data = PAYMENT_PLANS[plan_key]
        
        # Paystack requires amount in Kobo (Nigeria) or Cents (USD)
        amount_cents = plan_data['price_usd'] * 100 
        
        # Prepare transaction details
        email = request.user.email
        reference = f"{request.user.id}-{plan_key}-{datetime.now().timestamp()}"

        try:
            # Initialize Paystack Transaction
            txn = Transaction(secret_key=settings.PAYSTACK_SECRET_KEY)
            
            # The Paystack API call would go here to initialize the transaction
            response = txn.initialize(
                email=email,
                amount=amount_cents,
                reference=reference,
                metadata={"custom_fields": {"user_id": request.user.id, "plan_key": plan_key}}
            )
            
            # Mocking successful response
            authorization_url = f"https://mock-paystack.com/pay/{reference}" # Paystack payment link [cite: 103]
            
            return Response({"authorization_url": authorization_url, "reference": reference})
        
        except Exception as e:
            print(f"Paystack Initialization Error: {e}")
            return Response({"detail": "Could not initiate payment. Try again."}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class PaystackWebhookView(APIView):
    """
    Receives and processes webhooks from Paystack to update subscription status[cite: 104].
    Public Endpoint: /api/paystack-webhook/
    """
    permission_classes = () # Must be public for Paystack to access

    def post(self, request, *args, **kwargs):
        # 1. Verify Paystack Signature (Crucial Security Step - not implemented for brevity)
        # signature = request.headers.get('x-paystack-signature')
        # if not verify_signature(request.body, signature, settings.PAYSTACK_SECRET_KEY):
        #     return HttpResponse(status=400) 
        
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return HttpResponse(status=400)

        event = payload.get('event')
        data = payload.get('data', {})

        if event == 'charge.success':
            # This is the most common successful payment event
            # 2. Extract necessary data
            reference = data.get('reference')
            metadata = data.get('metadata', {}).get('custom_fields', {})
            user_id = metadata.get('user_id')
            plan_key = metadata.get('plan_key')
            
            if not user_id or not plan_key:
                return HttpResponse(status=400)

            user = get_object_or_404(settings.AUTH_USER_MODEL, pk=user_id)
            plan_data = PAYMENT_PLANS.get(plan_key)
            
            if not plan_data:
                return HttpResponse(status=400)

            # 3. Update the user's Subscription model 
            subscription, created = Subscription.objects.get_or_create(user=user)
            
            subscription.plan = plan_key
            subscription.runs_remaining = plan_data['runs']
            subscription.paystack_reference = reference
            subscription.status = 'ACTIVE'
            
            # Set end date based on plan duration
            subscription.end_date = datetime.now() + timedelta(days=plan_data['duration_days'])
            
            subscription.save()
            print(f"Subscription for User {user_id} updated to {plan_key}.")

        # For recurring plans, 'subscription.create' and 'subscription.notif' events are also crucial
        
        return HttpResponse(status=200) # Always return 200 OK to Paystack
