from PaymentStrategy import PaymentStrategy


class CashPayment(PaymentStrategy):
    def process_payment(self, amount: int) -> bool:
        # assume cash payment for now
        return True
