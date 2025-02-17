class PaymentStatus:
    def __init__(self, status_name: str):
        self.status_name = status_name

    def get_status(self) -> str:
        return self.status_name

# Concrete Payment Statuses
class SuccessPayment(PaymentStatus):
    def __init__(self):
        super().__init__("Success")

class FailedPayment(PaymentStatus):
    def __init__(self):
        super().__init__("Failed")

class InProgressPayment(PaymentStatus):
    def __init__(self):
        super().__init__("In Progress")
