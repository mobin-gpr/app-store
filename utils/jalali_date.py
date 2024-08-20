from jalali_date import date2jalali, datetime2jalali

jalali_months = {
    "01": "فرورودین",
    "02": "اردیبهشت",
    "03": "خرداد",
    "04": "تیر",
    "05": "مرداد",
    "06": "شهریور",
    "07": "مهر",
    "08": "آبان",
    "09": "آذر",
    "10": "دی",
    "11": "بهمن",
    "12": "اسفند",
}


def yyyy_mm_dd(date):
    return date2jalali(date).strftime("%Y/%m/%d")


def yyyy_month_dd(date):
    convert_georgian_month = date2jalali(date).strftime("%m")
    get_jalali_month = jalali_months.get(convert_georgian_month)
    return date2jalali(date).strftime(f"%d {get_jalali_month} %Y")


def yy_mm_dd(date):
    return date2jalali(date).strftime("%y/%m/%d")


def yy_month_dd(date):
    convert_georgian_month = date2jalali(date).strftime("%m")
    get_jalali_month = jalali_months.get(convert_georgian_month)
    return date2jalali(date).strftime(f"%d {get_jalali_month} %y")


def yyyy_mm_dd_hh_mm(date):
    return datetime2jalali(date).strftime("%H:%M - %Y/%m/%d")


def yyyy_month_dd_hh_mm(date):
    convert_georgian_month = date2jalali(date).strftime("%m")
    get_jalali_month = jalali_months.get(convert_georgian_month)
    return datetime2jalali(date).strftime(f"%H:%M - %d {get_jalali_month} %Y")


def yy_month_dd_hh_mm(date):
    convert_georgian_month = date2jalali(date).strftime("%m")
    get_jalali_month = jalali_months.get(convert_georgian_month)
    return datetime2jalali(date).strftime(f"%H:%M - %d {get_jalali_month} %y")


def yy_mm_dd_hh_mm(date):
    return datetime2jalali(date).strftime("%H:%M - %y/%m/%d")


def yyyy_month_dd_clock_HH_MM(date):
    convert_georgian_month = date2jalali(date).strftime("%m")
    get_jalali_month = jalali_months.get(convert_georgian_month)
    return datetime2jalali(date).strftime(f"%d {get_jalali_month} %Y ساعت %H:%M")
