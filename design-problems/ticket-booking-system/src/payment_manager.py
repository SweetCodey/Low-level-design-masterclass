class PaymentManager:
    def process_payment(self, user_id: int, amount: float) -> bool:
        """
        Process a payment for a user.
        """
        # For simplicity, we are assuming that the payment is successful
        print(f"Payment of {amount} processed for user {user_id}")
        return True
