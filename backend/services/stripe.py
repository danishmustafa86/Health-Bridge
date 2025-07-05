"""
Stripe Payment Service
Handles payment processing using Stripe API
"""
import stripe
import os
from typing import Dict, Any
from fastapi import HTTPException, status

class StripeService:
    """Stripe payment service class"""
    
    def __init__(self):
        """Initialize Stripe service with API key"""
        self.stripe_secret_key = os.getenv("STRIPE_SECRET_KEY")
        if not self.stripe_secret_key:
            raise ValueError("STRIPE_SECRET_KEY environment variable is required")
        
        stripe.api_key = self.stripe_secret_key
    
    async def create_payment_intent(
        self,
        amount: int,
        currency: str = "usd",
        payment_method: str = None,
        description: str = None,
        metadata: Dict[str, Any] = None
    ) -> stripe.PaymentIntent:
        """
        Create a payment intent for processing payment
        
        Args:
            amount: Amount in cents (e.g., 1000 for $10.00)
            currency: Currency code (default: "usd")
            payment_method: Payment method ID
            description: Payment description
            metadata: Additional metadata
        
        Returns:
            stripe.PaymentIntent: Created payment intent
        """
        try:
            intent_data = {
                "amount": amount,
                "currency": currency,
                "automatic_payment_methods": {
                    "enabled": True
                }
            }
            
            if payment_method:
                intent_data["payment_method"] = payment_method
                intent_data["confirm"] = True
            
            if description:
                intent_data["description"] = description
            
            if metadata:
                intent_data["metadata"] = metadata
            
            payment_intent = stripe.PaymentIntent.create(**intent_data)
            return payment_intent
        
        except stripe.error.CardError as e:
            # Card was declined
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Payment failed: {e.user_message}"
            )
        
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid payment request: {str(e)}"
            )
        
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Payment service authentication failed"
            )
        
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Payment service connection failed"
            )
        
        except stripe.error.StripeError as e:
            # Generic Stripe error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Payment processing failed: {str(e)}"
            )
    
    async def confirm_payment_intent(self, payment_intent_id: str) -> stripe.PaymentIntent:
        """
        Confirm a payment intent
        
        Args:
            payment_intent_id: Payment intent ID to confirm
        
        Returns:
            stripe.PaymentIntent: Confirmed payment intent
        """
        try:
            payment_intent = stripe.PaymentIntent.confirm(payment_intent_id)
            return payment_intent
        
        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Payment confirmation failed: {str(e)}"
            )
    
    async def retrieve_payment_intent(self, payment_intent_id: str) -> stripe.PaymentIntent:
        """
        Retrieve a payment intent
        
        Args:
            payment_intent_id: Payment intent ID
        
        Returns:
            stripe.PaymentIntent: Retrieved payment intent
        """
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return payment_intent
        
        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve payment: {str(e)}"
            )
    
    async def create_customer(self, email: str, name: str = None) -> stripe.Customer:
        """
        Create a Stripe customer
        
        Args:
            email: Customer email
            name: Customer name (optional)
        
        Returns:
            stripe.Customer: Created customer
        """
        try:
            customer_data = {"email": email}
            if name:
                customer_data["name"] = name
            
            customer = stripe.Customer.create(**customer_data)
            return customer
        
        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create customer: {str(e)}"
            )
    
    async def refund_payment(
        self,
        payment_intent_id: str,
        amount: int = None,
        reason: str = None
    ) -> stripe.Refund:
        """
        Create a refund for a payment
        
        Args:
            payment_intent_id: Payment intent ID to refund
            amount: Refund amount in cents (optional, full refund if not specified)
            reason: Refund reason (optional)
        
        Returns:
            stripe.Refund: Created refund
        """
        try:
            refund_data = {"payment_intent": payment_intent_id}
            
            if amount:
                refund_data["amount"] = amount
            
            if reason:
                refund_data["reason"] = reason
            
            refund = stripe.Refund.create(**refund_data)
            return refund
        
        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Refund failed: {str(e)}"
            )
    
    async def get_payment_methods(self, customer_id: str) -> List[stripe.PaymentMethod]:
        """
        Get all payment methods for a customer
        
        Args:
            customer_id: Stripe customer ID
        
        Returns:
            List[stripe.PaymentMethod]: List of payment methods
        """
        try:
            payment_methods = stripe.PaymentMethod.list(
                customer=customer_id,
                type="card"
            )
            return payment_methods.data
        
        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get payment methods: {str(e)}"
            )
    
    def construct_webhook_event(self, payload: str, sig_header: str) -> stripe.Event:
        """
        Construct webhook event from Stripe
        
        Args:
            payload: Raw request payload
            sig_header: Stripe signature header
        
        Returns:
            stripe.Event: Constructed webhook event
        """
        webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        if not webhook_secret:
            raise ValueError("STRIPE_WEBHOOK_SECRET environment variable is required")
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
            return event
        
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid payload"
            )
        
        except stripe.error.SignatureVerificationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid signature"
            )