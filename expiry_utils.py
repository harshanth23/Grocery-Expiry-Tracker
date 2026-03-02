from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculate_expiry(mfg_date: str, unit: str, amount: int) -> str:
    """
    Expiry = MFG/PKD + selected duration
    """
    mfg_date = mfg_date.replace("/", "-")
    mfg = datetime.strptime(mfg_date, "%d-%m-%Y")

    if unit == "days":
        expiry = mfg + relativedelta(days=amount)
    elif unit == "months":
        expiry = mfg + relativedelta(months=amount)
    else:
        raise ValueError("Invalid validity unit")

    return expiry.strftime("%d-%m-%Y")
