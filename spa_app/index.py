import os
from flask import Flask, render_template, request, redirect, session, jsonify
from spa_app import db, app, utils
from spa_app.dao import load_therapists, load_appointments, get_appointment_details, change_appointment_status, \
    assign_therapists, update_sheet_detail, check_discount, load_service_sheets, get_service_sheet_details
from spa_app.models import DatLich, DatLichDetail, PhieuDichVu, PhieuDichVuDetail, HoaDon, TrangThaiDatLich

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
    appointments = load_appointments()
    appointment_details = None
    therapists = None
    if id > 0:
        appointment_details = get_appointment_details(id)
        if appointment_details[0].dat_lich.trang_thai_dat_lich==TrangThaiDatLich.CHO_XAC_NHAN:
            therapists = load_therapists()

    return render_template("appointments.html", pages=1, id=id, kw=kw,
                           appointments=appointments,
                           appointment_details=appointment_details,
                           therapists=therapists)

@app.route('/appointments/<int:id>/success', methods=['POST'])
def success_appointment(id):
    data = request.get_json()

    if not data or 'selectedTherapists' not in data:
        return jsonify({"status": 400, "err_msg": "Dữ liệu không tồn tại"})

    selected_therapists = data['selectedTherapists']

    check = assign_therapists(id, selected_therapists)
    if check==-1:
        return jsonify({"status": 400, "err_msg": "Dữ liệu không hợp lệ"})

    change_appointment_status(id, TrangThaiDatLich.DA_XAC_NHAN)

    return jsonify({
        "status": 200,
    })

@app.route('/appointments/<int:id>/carryOut')
def carry_out_appointment(id):
    change_appointment_status(id, TrangThaiDatLich.DANG_THUC_HIEN)
    return redirect('/appointments/'+ str(id))

@app.route('/appointments/<int:id>/cancel')
def cancel_appointment(id):
    change_appointment_status(id, TrangThaiDatLich.DA_HUY)
    return redirect('/appointments/'+ str(id))

@app.route('/serviceSheets/<int:id>')
def service_sheet(id):
    kw = request.args.get("search")
    appointments = DatLich.query.all()
    appointment_details = get_appointment_details(id)
    service_sheet_details = None
    if id > 0:
        if load_service_sheets(appointment_id=id):
            sheet = load_service_sheets(appointment_id=id)
            service_sheet_details = get_service_sheet_details(sheet.id)
    return render_template("serviceSheets.html", pages=1, id=id, kw=kw,
                           service_sheet_details=service_sheet_details,
                           appointments=appointments,
                           appointment_details=appointment_details)

@app.route('/serviceSheets/update/<int:id>')
def update_service_sheet(id):
    flag = True
    kw = request.args.get("search")
    appointments = DatLich.query.all()
    appointment_details = get_appointment_details(id)
    service_sheet_details = None
    if load_service_sheets(appointment_id=id):
        sheet = load_service_sheets(appointment_id=id)
        service_sheet_details = get_service_sheet_details(sheet.id)
    return render_template("serviceSheets.html", pages=1, id=id, kw=kw, flag=flag,
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
    service_sheets = PhieuDichVu.query.all()
    service_sheet_detail = None
    receipt = None
    invoice = None
    total_tmp = None

    if id > 0:
        service_sheet_detail = PhieuDichVuDetail.query.filter(PhieuDichVuDetail.ma_phieu_dich_vu == id).all()
        receipt = HoaDon.query.filter(HoaDon.ma_phieu_dich_vu == id).first()
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

    return render_template("invoices.html", pages=1, id=id, kw=kw, flag=flag,
                           service_sheets=service_sheets,
                           service_sheet_detail=service_sheet_detail,
                           receipt=receipt,
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
    if invoice and str(id) in invoice and str(discount.dich_vu.id) in invoice[str(id)]:
        if invoice[str(id)][str(discount.dich_vu.id)]["ma_giam_gia"] is not None:
            return jsonify({"status": 400, "err_msg": "Mã giảm giá đang được áp dụng"})
        invoice[str(id)][str(discount.dich_vu.id)]['ma_giam_gia']=discount.id
        invoice[str(id)][str(discount.dich_vu.id)]['muc_giam_gia']=discount.muc_giam_gia
        session.modified = True

    else:
        return jsonify({"status": 400, "err_msg": "Lỗi hệ thống"})

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
    print(invoice[str(id)])
    total_tmp = utils.total(invoice=invoice[str(id)])
    return render_template("invoices.html", id=id, flag=flag,
                           service_sheet_detail=service_sheet_detail,
                           invoice=invoice,
                           total_tmp=total_tmp)

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
