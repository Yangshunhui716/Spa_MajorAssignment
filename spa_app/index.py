from flask import Flask, render_template, request, session
from spa_app import db, app
from spa_app.models import DatLich, DatLichDetail


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/appointments/<int:id>')
def appointment(id):
    appointments = DatLich.query.all()
    appointment_chossen = DatLich.query.filter(DatLich.id == id).first()
    appointment_detail = None
    if id != 0:
        appointment_detail = DatLichDetail.query.filter(DatLichDetail.ma_dat_lich == id).all()
        print(appointment_detail)

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
        print(appointment_detail)
    kw = request.args.get("search")
    flag = True
    if kw is None:
        return render_template("appointments.html", pages=1, id=id, appointment_chossen=appointment_chossen,
                               appointments=appointments, appointment_detail=appointment_detail, flag=flag)
    return render_template("appointments.html", pages=1, id=id, kw=kw, appointment_chossen=appointment_chossen,
                           appointments=appointments, appointment_detail=appointment_detail, flag=flag)


@app.route('/serviceSheets/<int:id>')
def service_sheet(id):
    kw = request.args.get("search")
    if kw is None:
        return render_template("serviceSheets.html", pages=1, id=id)
    return render_template("serviceSheets.html", pages=1, id=id, kw=kw)


@app.route('/serviceSheets/update/<int:id>')
def update_service_sheet(id):
    kw = request.args.get("search")
    flag = True
    if kw is None:
        return render_template("serviceSheets.html", pages=1, id=id, flag=flag)
    return render_template("serviceSheets.html", pages=1, id=id, kw=kw, flag=flag)


@app.route('/payments/<int:id>')
def payment(id):
    kw = request.args.get("search")
    if kw is None:
        return render_template("payments.html", pages=1, id=id)
    return render_template("payments.html", pages=1, id=id, kw=kw)


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
