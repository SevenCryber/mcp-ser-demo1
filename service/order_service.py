from clients.base import BaseClient
from auth.auth import HRAuth
from models.hr import EmployeeDTO

class OrderService(BaseClient):
    def __init__(self):
        super().__init__()

    async def get_employee(self, emp_id: str, user_id: str) -> EmployeeDTO:
        r = await self._request("GET", f"/employees/{emp_id}", user_id)
        return EmployeeDTO.parse_obj(r.json())