from clients.base import BaseClient
from auth.auth import HRAuth
from settings import settings
from models.hr import EmployeeDTO

class HRClient(BaseClient):
    def __init__(self):
        super().__init__(auth=HRAuth(), base_url=str(settings.hr_base_url))

    async def get_employee(self, emp_id: str, user_id: str) -> EmployeeDTO:
        r = await self._request("GET", f"/employees/{emp_id}", user_id)
        return EmployeeDTO.parse_obj(r.json())