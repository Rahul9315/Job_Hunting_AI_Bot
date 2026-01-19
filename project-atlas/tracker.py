from openpyxl import Workbook, load_workbook
from datetime import datetime
import os


FILE = "data/applied.xlsx"




def log(job, status):
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(FILE):
        wb = Workbook()
        ws = wb.active
        ws.append(["Date", "Platform", "Company", "Role", "Location", "Status", "Link"])
        wb.save(FILE)


    wb = load_workbook(FILE)
    ws = wb.active
    ws.append([
        datetime.now().strftime("%Y-%m-%d"),
        job.get("platform"),
        job.get("company"),
        job.get("title"),
        job.get("location"),
        status,
        job.get("link")
    ])
    wb.save(FILE)