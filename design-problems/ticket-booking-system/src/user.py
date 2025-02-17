from typing import List
from ticket import Ticket

class User:
    def __init__(self, user_id: int, name: str, email: str, phone: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.tickets: List[Ticket] = []
