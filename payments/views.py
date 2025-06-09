from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PaymentSerializer
from .models import Payment
from .paystack import PaystackAPI



class InitiatePaymentView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': 'Invalid data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        paystack_response = PaystackAPI.initiate_payment(
            email=data['customer_email'],
            amount=data['amount'],
            name=data['customer_name']
        )

        if paystack_response.get('status') is not True:
            return Response({
                'status': False,
                'message': 'Payment initiation failed',
                'error': paystack_response.get('message', 'Unknown error')
            }, status=status.HTTP_400_BAD_REQUEST)

        reference = paystack_response['data']['reference']
        Payment.objects.create(
            reference=reference,
            amount=data['amount'],
            customer_email=data['customer_email'],
            customer_name=data['customer_name'],
            status='pending'
        )

        return Response({
            'status': True,
            'message': 'Payment initiated successfully',
            'data': paystack_response['data']
        }, status=status.HTTP_200_OK)
        

class PaymentStatusView(APIView):
    def get(self, request, payment_id):
        try:
            payment = Payment.objects.get(reference=payment_id)
        except Payment.DoesNotExist:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Payment not found'
            }, status=status.HTTP_404_NOT_FOUND)
            
        paystack_response = PaystackAPI.verify_payment(payment.reference)
        if paystack_response.get('status'):
            payment.status = paystack_response['data']['status']
            payment.save()
            
            response_data = {
                "payment": {
                    "id": payment.reference,
                    "customer_email": payment.customer_email,
                    "customer_name": payment.customer_name,
                    "amount": payment.amount,
                    "status": payment.status,
                },
                "status": status.HTTP_200_OK,
                "message": "Payment status retrieved successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(paystack_response, status=status.HTTP_400_BAD_REQUEST)