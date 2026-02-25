from PaymentStrategy import PaymentStrategy


class CashPayment(PaymentStrategy):
    def process_payment(self, amount: int) -> bool:
        print(f"  Payment of Rs.{amount} processed via cash.")
        return True
