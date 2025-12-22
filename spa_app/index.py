import math
from flask import render_template, request, redirect, session, jsonify
from spa_app import app, utils
from spa_app.dao import load_appointments, get_appointment_details, change_appointment_status, \
    assign_therapists, update_sheet_detail, check_discount, load_service_sheets, get_service_sheet_details, \
    count_appointments, count_service_sheets, get_free_therapists_list, add_busy_time, assign_receptionist, \
    get_appointment_status, get_receipt, del_busy_time, get_vat, add_receipt, get_receipt_discount
from spa_app.models import HoaDon, TrangThaiDatLich

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def index_services():
    return render_template('index_services.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/appointments/<int:id>')
def appointment(id):
    kw = request.args.get("search")
    status = request.args.get("status")
    if status == None:
        status = 'LE_TAN'
    page = int(request.args.get("page"))
    pages = math.ceil(count_appointments(status=status, kw=kw) / app.config["PAGE_SIZE"])

    appointments = load_appointments(status=status, kw=kw, page=page)
    appointment_details = None
    therapists = None

    if id > 0:
        appointment_details = get_appointment_details(appointment_id=id)
        if get_appointment_status(appointment_id=appointment_details[0].dat_lich.id)==TrangThaiDatLich.CHO_XAC_NHAN:
            therapists = get_free_therapists_list(appointment_details=appointment_details)

    return render_template("appointments.html", pages=pages, page=page, id=id, kw=kw, status=status,
                           appointments=appointments,
                           appointment_details=appointment_details,
                           therapists=therapists)

@app.route('/appointments/<int:id>/success', methods=['POST'])
def success_appointment(id):
    data = request.get_json()

    if not data or 'selectedTherapists' not in data:
        return jsonify({"status": 400, "err_msg": "Dữ liệu không tồn tại"})

    selected_therapists = data['selectedTherapists']

    check = assign_therapists(appointment_id=id, selected_therapists=selected_therapists)
    if check==-1:
        return jsonify({"status": 400, "err_msg": "Dữ liệu không hợp lệ"})

    add_busy_time(appointment_id=id, selected_therapists=selected_therapists)
    assign_receptionist(appointment_id=id, receptionist_id=5)
    change_appointment_status(appointment_id=id, status=TrangThaiDatLich.DA_XAC_NHAN)

    return jsonify({
        "status": 200,
    })

@app.route('/appointments/<int:id>/carryOut')
def carry_out_appointment(id):
    change_appointment_status(appointment_id=id, status=TrangThaiDatLich.DANG_THUC_HIEN)
    return redirect('/appointments/0?status=LE_TAN&page=1')

@app.route('/appointments/<int:id>/cancel')
def cancel_appointment(id):
    del_busy_time(appointment_id=id)
    change_appointment_status(appointment_id=id, status=TrangThaiDatLich.DA_HUY)
    return redirect('/appointments/' + str(id) + '?status=LE_TAN&page=1')

@app.route('/serviceSheets/<int:id>')
def service_sheet(id):
    kw = request.args.get("search")
    status = request.args.get("status")
    hind = False
    if status == None:
        status = 'KTV'
    elif status == 'DA_XAC_NHAN':
        hind = True
    page = int(request.args.get("page"))
    pages = math.ceil(count_appointments(status=status, kw=kw, hind=hind) / app.config["PAGE_SIZE"])
    appointments = load_appointments(status=status, kw=kw, page=page, hind=hind)
    appointment_details = None
    service_sheet_details = None
    if id > 0:
        if load_service_sheets(appointment_id=id):
            sheet = load_service_sheets(appointment_id=id)
            service_sheet_details = get_service_sheet_details(service_sheet_id=sheet.id)
        appointment_details = get_appointment_details(appointment_id=id)
    return render_template("serviceSheets.html", pages=pages, page=page, id=id, kw=kw, status=status,
                           service_sheet_details=service_sheet_details,
                           appointments=appointments,
                           appointment_details=appointment_details)

@app.route('/serviceSheets/update/<int:id>')
def update_service_sheet(id):
    flag = True
    hind = False
    kw = request.args.get("search")
    status = request.args.get("status")
    if status == None:
        status = 'KTV'
    elif status == 'DA_XAC_NHAN':
        hind = True
    page = int(request.args.get("page"))
    pages = math.ceil(count_appointments(status=status, kw=kw, hind=hind) / app.config["PAGE_SIZE"])
    appointments = load_appointments(status=status, kw=kw, page=page, hind=hind)
    appointment_details = get_appointment_details(appointment_id=id)
    service_sheet_details = None
    if load_service_sheets(appointment_id=id):
        sheet = load_service_sheets(appointment_id=id)
        service_sheet_details = get_service_sheet_details(service_sheet_id=sheet.id)
    return render_template("serviceSheets.html", pages=pages, page=page, id=id, kw=kw, status=status, flag=flag,
                           service_sheet_details=service_sheet_details,
                           appointments=appointments,
                           appointment_details=appointment_details)


@app.route('/serviceSheets/update/<int:id>/success', methods=['POST'])
def success_service_sheet(id):
    data = request.get_json()
    if not data:
        return jsonify({"status": 400, "err_msg": "Dữ liệu không tồn tại"})

    update_sheet_detail(id, data)

    return jsonify({
        "status": 200,
    })

@app.route('/invoices/<int:id>')
def invoice(id):
    flag = False
    kw = request.args.get("search")
    page = int(request.args.get("page"))
    pages = math.ceil(count_service_sheets(kw, flag) / app.config["PAGE_SIZE"])

    service_sheets = load_service_sheets(kw=kw, page=page, flag=flag)
    service_sheet_detail = None
    receipt = None
    receipt_discount = None
    invoice = None
    total_tmp = None

    if id > 0:
        service_sheet_detail = get_service_sheet_details(service_sheet_id=id)
        receipt = get_receipt(service_sheet_id=id)

        if receipt is None:
            invoice = session.get('invoice', {})
            if str(id) not in invoice:
                invoice[str(id)] = {}
                for s in service_sheet_detail:
                    invoice[str(id)][str(s.dich_vu.id)] = {
                        "ma_giam_gia": None,
                        "muc_giam_gia": 0,
                        "ma_dich_vu": s.dich_vu.id,
                        "gia_dich_vu": s.dich_vu.gia_dich_vu,
                    }
                session["invoice"] = invoice
                session.modified = True
            total_tmp = utils.total(invoice=invoice[str(id)])

        else: receipt_discount = get_receipt_discount(receipt_id = receipt.id)

    return render_template("invoices.html", pages=pages, page=page, id=id, kw=kw, flag=flag,
                           service_sheets=service_sheets,
                           service_sheet_detail=service_sheet_detail,
                           receipt=receipt,
                           receipt_discount=receipt_discount,
                           invoice=invoice,
                           total_tmp=total_tmp)

@app.route('/invoices/<int:id>/add_discount', methods=['PUT'])
def add_discount(id):
    discount = check_discount(request.json.get("ma_giam_gia"), request.json.get("ma_khach_hang"))
    if discount==-1:
        return jsonify({"status": 400, "err_msg": "Mã giảm giá không hợp lệ"})
    elif discount==0:
        return jsonify({"status": 400, "err_msg": "Mã giảm giá hết hạn sử dụng"})

    invoice = session.get('invoice', {})
    print(invoice)
    if invoice and str(id) in invoice and str(discount.dich_vu.id) in invoice[str(id)]:
        if invoice[str(id)][str(discount.dich_vu.id)]["ma_giam_gia"] is not None:
            return jsonify({"status": 400, "err_msg": "Mã giảm giá đang được áp dụng"})
        invoice[str(id)][str(discount.dich_vu.id)]['ma_giam_gia']=discount.id
        invoice[str(id)][str(discount.dich_vu.id)]['muc_giam_gia']=discount.muc_giam_gia
        session.modified = True

    else:
        return jsonify({"status": 400, "err_msg": "Mã giảm giá không hợp lệ"})

    return jsonify(utils.total(invoice=invoice[str(id)]))


@app.route('/invoices/<int:id>/remove_discount', methods=['PUT'])
def remove_discount(id):
    invoice = session.get('invoice', {})
    service_id = request.json.get("ma_dich_vu")

    if invoice and str(id) in invoice and str(service_id) in invoice[str(id)]:
        if invoice[str(id)][str(service_id)]["ma_giam_gia"] is None:
            return jsonify({"status": 400, "err_msg": "Dịch vụ đang không sử dụng mã giảm giá"})
        else :
            invoice[str(id)][str(service_id)]["ma_giam_gia"] = None
            invoice[str(id)][str(service_id)]["muc_giam_gia"] = 0
            session.modified = True
    else:
        return jsonify({"status": 400, "err_msg": "Lỗi hệ thống"})

    return jsonify(utils.total(invoice=invoice[str(id)]))


@app.route('/invoices/<int:id>/payment')
def payment(id):
    flag=True
    service_sheet_detail = get_service_sheet_details(service_sheet_id=id)
    invoice = session.get('invoice', {})
    total_tmp = utils.total(invoice=invoice[str(id)])
    return render_template("invoices.html", id=id, flag=flag,
                           service_sheet_detail=service_sheet_detail,
                           invoice=invoice,
                           total_tmp=total_tmp)


@app.route('/invoices/<int:id>/payment/success', methods=['POST'])
def success_pay(id):
    invoice = session.get('invoice', {})
    payment_method = request.json.get("phuong_thuc")
    temporary = request.json.get("tong_dich_vu")
    total_discount = request.json.get("tong_giam_gia")
    total_amount = request.json.get("tong_thanh_toan")
    paid = request.json.get("so_tien_nhan")
    customer_id = load_service_sheets(sheet_id=id).dat_lich.khach_hang.id

    try:
        add_receipt(customer_id=customer_id, invoice=invoice[str(id)], payment_method=payment_method,
                    temporary=temporary, total_discount=total_discount, total_amount=total_amount,
                    paid=paid, sheet_id=id, cashier_id=6)
    except Exception as ex:
        return jsonify({"status": 500, "err_msg": str(ex)})
    else:
        del session['invoice'][str(id)]
        session.modified = True
        return jsonify({"status": 200})


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
