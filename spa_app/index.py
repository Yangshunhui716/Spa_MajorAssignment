import os
from flask import Flask, render_template, request, session
from spa_app import db, app
from spa_app.models import DatLich, DatLichDetail, PhieuDichVu, PhieuDichVuDetail, HoaDon


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
    appointments = DatLich.query.all()
    appointment_chossen = DatLich.query.filter(DatLich.id == id).first()
    appointment_detail = None
    if id != 0:
        appointment_detail = DatLichDetail.query.filter(DatLichDetail.ma_dat_lich == id).all()

    kw = request.args.get("search")
    if kw is None:
        return render_template("appointments.html", pages=1, id=id, appointment_chossen=appointment_chossen,
                               appointments=appointments, appointment_detail=appointment_detail)
    return render_template("appointments.html", pages=1, id=id, kw=kw, appointment_chossen=appointment_chossen,
                           appointments=appointments, appointment_detail=appointment_detail)


@app.route('/appointments/update/<int:id>')
def update_appointment(id):
    appointments = DatLich.query.all()
    appointment_chossen = DatLich.query.filter(DatLich.id == id).first()
    appointment_detail = None
    if id != 0:
        appointment_detail = DatLichDetail.query.filter(DatLichDetail.ma_dat_lich == id).all()
    kw = request.args.get("search")
    flag = True
    if kw is None:
        return render_template("appointments.html", pages=1, id=id, appointment_chossen=appointment_chossen,
                               appointments=appointments, appointment_detail=appointment_detail, flag=flag)
    return render_template("appointments.html", pages=1, id=id, kw=kw, appointment_chossen=appointment_chossen,
                           appointments=appointments, appointment_detail=appointment_detail, flag=flag)


@app.route('/serviceSheets/<int:id>')
def service_sheet(id):
    appointment_detail = DatLichDetail.query.all()
    appointments = DatLich.query.all()
    service_sheet = None
    service_sheet_detail = None

    if id != 0:
        service_sheet = PhieuDichVu.query.filter(PhieuDichVu.ma_dat_lich == id).first()
        service_sheet_detail = PhieuDichVuDetail.query.filter(
            PhieuDichVuDetail.ma_phieu_dich_vu == service_sheet.id).all()
    kw = request.args.get("search")
    if kw is None:
        return render_template("serviceSheets.html", pages=1, id=id, service_sheet_detail=service_sheet_detail,
                               appointments=appointments,
                               appointment_detail=appointment_detail,
                               service_sheet=service_sheet)
    return render_template("serviceSheets.html", pages=1, service_sheet_detail=service_sheet_detail, id=id, kw=kw,
                           appointments=appointments,
                           appointment_detail=appointment_detail,
                           service_sheet=service_sheet)


@app.route('/serviceSheets/update/<int:id>')
def update_service_sheet(id):
    appointments = DatLich.query.all()
    services_sheets = PhieuDichVu.query.first()
    appointment_detail = None

    if id != 0:
        appointment_detail = DatLichDetail.query.filter(DatLichDetail.ma_dat_lich == id).all()
    kw = request.args.get("search")
    flag = True
    if kw is None:
        return render_template("serviceSheets.html", pages=1, id=id, appointments=appointments,
                               appointment_detail=appointment_detail,
                               services_sheets=services_sheets, flag=flag)
    return render_template("serviceSheets.html", pages=1, id=id, kw=kw, appointments=appointments,
                           appointment_detail=appointment_detail,
                           services_sheets=services_sheets, flag=flag)


@app.route('/payments/<int:id>')
def payment(id):
    service_sheets = PhieuDichVu.query.all()
    receipt = HoaDon.query.filter(HoaDon.ma_phieu_dich_vu == id).first()
    if (receipt == None):
        receipt_tmp = PhieuDichVu.query.filter(PhieuDichVu.id == id).first
    recipt_detail = PhieuDichVuDetail.query.filter(PhieuDichVuDetail.ma_phieu_dich_vu == id).all()
    service_sheet_detail = None

    if id != 0:
        appointment_detail = DatLichDetail.query.filter(DatLichDetail.ma_dat_lich == id).all()

    kw = request.args.get("search")
    if kw is None:
        return render_template("payments.html", pages=1, id=id, receipt=receipt,
                               service_sheets = service_sheets,
                               recipt_detail=recipt_detail,
                               service_sheet_detail=service_sheet_detail)
    return render_template("payments.html", pages=1, id=id, kw=kw, receipt=receipt,
                           service_sheets=service_sheets,
                           recipt_detail=recipt_detail,
                           service_sheet_detail=service_sheet_detail)


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
