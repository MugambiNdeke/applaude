from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class ContactSubmitView(APIView):
    """
    Handles the contact form submission from the landing page.
    """
    permission_classes = (AllowAny,) # Public endpoint

    def post(self, request):
        # In a real application, you would use a serializer to validate the data
        name = request.data.get('name')
        email = request.data.get('email')
        message = request.data.get('message')

        if not all([name, email, message]):
            return Response({"detail": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # --- Placeholder for Business Logic ---
        # 1. Log the message to the database (e.g., a ContactMessage model)
        # 2. Send an email notification to the Applaude team (e.g., via Django's send_mail)
        print(f"NEW CONTACT SUBMISSION from {name} ({email}): {message[:50]}...")
        # -------------------------------------

        return Response({"detail": "Thank you! Your message has been received."}, 
                        status=status.HTTP_200_OK)
