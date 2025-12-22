from spa_app.dao import get_vat

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
