import os
from flask import Flask, render_template, request, redirect, session, jsonify
from spa_app import db, app
from spa_app.dao import load_therapists, load_services, load_appointments, get_appointment_details, change_appointment_status, assign_therapists, update_sheet_detail
from spa_app.models import DatLich, DatLichDetail, PhieuDichVu, PhieuDichVuDetail, HoaDon, TrangThaiDatLich

@app.route('/')
def index():
    image_folder = os.path.join(app.static_folder, "images")
    images = os.listdir(image_folder)
    return render_template('index.html', images=images)

@app.route('/index_services')
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
        if appointment_details[0].dat_lich.trang_thai_dat_lich == TrangThaiDatLich.CHO_XAC_NHAN:
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
    if check == -1:
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
        if PhieuDichVu.query.filter(PhieuDichVu.ma_dat_lich == id).first():
            service_sheet_details = PhieuDichVuDetail.query.filter(PhieuDichVuDetail.ma_phieu_dich_vu == id).all()
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
    service_sheet_details = PhieuDichVuDetail.query.filter(PhieuDichVuDetail.ma_phieu_dich_vu == id).all()
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

@app.route('/payments/<int:id>')
def payment(id):
    service_sheets = PhieuDichVu.query.all()
    service_sheet_detail = None
    receiption = None
    total_payment = None

    if id > 0:
        receiption = HoaDon.query.filter(HoaDon.ma_phieu_dich_vu == id).first()
        if receiption is not None:
            total_payment = receiption.tong_thanh_toan
        else:
            total_payment = 0
        service_sheet_detail = PhieuDichVuDetail.query.filter(PhieuDichVuDetail.ma_phieu_dich_vu == id).all()

    kw = request.args.get("search")
    return render_template("payments.html", pages=1, id=id, kw=kw,
                           receiption=receiption,
                           service_sheets=service_sheets,
                           service_sheet_detail=service_sheet_detail,
                           total_payment=total_payment)


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
