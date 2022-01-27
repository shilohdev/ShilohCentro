from datetime import timedelta
from dateutil.relativedelta import relativedelta
from datetime import datetime

#FILTRO DO MES
def dealStrignify(self):
    y = ""
    for k in self:
        y += k + ", "
    return y[:-2]


def convertDate(indexable):
    indexable = str(indexable)
    if "+" in indexable:
        indexable = indexable.split("+")[0]

    if indexable is None:
        d = ""
        
    elif indexable == "":
        d = ""

    elif len(indexable) == 19:
        d = datetime.strptime(indexable, '%Y-%m-%d %H:%M:%S')
        d = d.strftime('%d/%m/%Y %H:%M:%S')

    elif len(indexable) == 10:
        d = datetime.strptime(indexable, '%Y-%m-%d')
        d = d.strftime('%d/%m/%Y')

    else:
        d = ""
    
    return d


def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - timedelta(days=1)


def checkDayMonth(e):
    dayNow = str(datetime.today().weekday())

    if e == "this_month":
        dt_start = str(datetime.now().strftime("%Y-%m-")) + "01"
        dt_end = str(last_day_of_month(datetime.today()).strftime("%Y-%m-%d"))

    elif e == "last_month":
        l_month = datetime.now() - relativedelta(months=1)
        dt_start = str(l_month.strftime("%Y-%m-")) + "01"
        dt_end = str(last_day_of_month(l_month).strftime("%Y-%m-%d"))

    return {"dt_start": dt_start, "dt_end": dt_end}