from spa_app.dao import get_vat, get_busy_time
from datetime import datetime


def total(invoice):
    temporary, total_discount, total_amount = 0, 0, 0
    vat = get_vat()
    service_list = []

    if invoice:
        for s in invoice.values():
            service_list.append(s)
        for i in service_list:
            temporary += i["gia_dich_vu"]
            total_discount += (i["gia_dich_vu"]*(i["muc_giam_gia"]))
        total_amount = (temporary - total_discount)*(1+(vat.muc_vat))

    return {
        "status": 200,
        "temporary": temporary,
        "total_discount": total_discount,
        "vat": vat.muc_vat,
        "total_amount": total_amount,
    }


def present_service(appointment_id):
    busy_time_of_appointment = get_busy_time(appointment_id=appointment_id)
    present_time = datetime.now()
    if busy_time_of_appointment:
        for b in busy_time_of_appointment:
            if present_time >= b.thoi_gian_bat_dau:
                return b
    return None


def next_service(appointment_id):
    busy_time_of_appointment = get_busy_time(appointment_id=appointment_id)
    present_time = datetime.now()
    if busy_time_of_appointment:
        before=None
        for b in busy_time_of_appointment:
            if present_time >= b.thoi_gian_bat_dau:
                return before
            before = b
    return None