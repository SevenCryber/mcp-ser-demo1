from fastapi import APIRouter
from clients.hr import HRClient
from clients.finance import FinanceClient

router = APIRouter()

@router.get("/report/{emp_id}")
async def make_report(emp_id: str):
    # 并发调外部
    async with HRClient() as hr, FinanceClient() as finance:
        emp, salary = await asyncio.gather(
            hr.get_employee(emp_id),
            finance.get_salary(emp_id),
        )
    return {
        "name": emp.name,
        "dept": emp.department,
        "salary": salary.monthly,
    }