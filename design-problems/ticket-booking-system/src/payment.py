from payment_status import PaymentStatus

class Payment:
    def __init__(self, payment_id: int, ticket_id: int, amount: float, 
                 payment_method: str, payment_status: PaymentStatus):
        self.payment_id = payment_id
        self.ticket_id = ticket_id
        self.amount = amount
        self.payment_method = payment_method  # Credit/Debit
        self.payment_status = payment_status
