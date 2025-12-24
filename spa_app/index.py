import math
from flask import render_template, request, redirect, session, jsonify, url_for
from flask_login import login_user, logout_user, current_user, login_required
from spa_app import db, app, utils, login_manager, admin
from spa_app.dao import load_appointments, get_appointment_details, change_appointment_status, \
    assign_therapists, update_sheet_detail, check_discount, load_service_sheets, get_service_sheet_details, \
    count_appointments, count_service_sheets, get_free_therapists_list, add_busy_time, assign_receptionist, \
    get_appointment_status, get_receipt, del_busy_time, add_receipt, get_receipt_discount, auth_user, \
    add_user, get_user_by_id, is_ky_thuat_vien, get_user_by_phone, get_user_by_username, add_dat_lich, \
    add_dat_lich_detail, get_busy_time
from spa_app.models import DatLich, TrangThaiDatLich, UserRole, User, DatLichDetail, DichVu, PhieuDichVuDetail, \
    PhieuDichVu, KyThuatVien
from datetime import datetime, timedelta
from spa_app.decorators import anonymous_required
import cloudinary.uploader
from spa_app.utils import present_service, next_service


@app.route('/')
def index():
    dich_vu_list = DichVu.query.all()

    list_services = [
        {
            "id": dv.id,
            "ten": dv.ten_dich_vu,
            "thoi_gian": dv.thoi_gian_dich_vu
        }
        for dv in dich_vu_list
    ]

    return render_template(
        'index.html',
        dich_vu_list=dich_vu_list,
        list_services=list_services
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    err_msg = None
    if request.method == "POST":
        password = request.form.get("password")
        confirm = request.form.get("confirm_password")

        if password == confirm:
            name = request.form.get("name")
            username = request.form.get("username")
            email = request.form.get("email")
            phone = request.form.get("phone")

            existing_phone = get_user_by_phone(phone)
            if existing_phone:
                err_msg = "Số điện thoại đã được sử dụng!"
            else:
                existing_username = get_user_by_username(username)
                if existing_username:
                    err_msg = "Tên tài khoản đã tồn tại!"
                else:
                    add_user(name=name, username=username, password=password,
                             email=email, phone=phone)
        else:
            err_msg = "Mật khẩu không khớp!"

    return render_template('register.html', err_msg=err_msg)


@app.route("/login", methods=["GET", "POST"])
@anonymous_required
def login():
    err_msg = None
    if request.method.__eq__("POST"):
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        user = auth_user(username, password)

        if user:
            login_user(user)
            role = user.role_user
            print("LOGIN USER:")
            print(" - id:", user.id)
            print(" - username:", user.tai_khoan_user)
            print(" - role:", user.role_user)

            ktv = is_ky_thuat_vien(user.id)
            if ktv:
                return redirect((url_for("service_sheet", id=0, page=1)))

            if role == UserRole.USER:
                return redirect((url_for("index")))

            if role == UserRole.KY_THUAT_VIEN:
                return redirect((url_for("service_sheet", id = 0, page=1, status='KTV')))

            if role == UserRole.LE_TAN:
                return redirect((url_for("appointment", id = 0, page=1, status='LE_TAN')))

            if role == UserRole.THU_NGAN:
                return redirect((url_for("invoice", id=0, page=1)))

            next = request.args.get("next")
            return redirect(next if next else "/")
        else:
            err_msg = "Tài khoản hoặc mật khẩu không đúng!"

    return render_template("login.html", err_msg=err_msg)


@app.route("/logout")
def logout_my_user():
    logout_user()
    return redirect("/login")


@login_manager.user_loader
def get_user(user_id):
    return get_user_by_id(user_id=user_id)


@app.route("/admin-login", methods=["POST"])
def admin_login_process():
    username = request.form.get("username")
    password = request.form.get("password")

    user = auth_user(username, password)

    if user:
        login_user(user)
        return redirect("/admin")
    else:
        err_msg = "Tài khoản hoặc mật khẩu không đúng!"


@app.route('/services')
def index_services():
    dich_vu_list = DichVu.query.all()

    return render_template('index_services.html', dich_vu_list=dich_vu_list)


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    # ---------- GET ----------
    if request.method == 'GET':
        dich_vu_list = DichVu.query.all()

        list_services = [
            {
                "id": dv.id,
                "ten": dv.ten_dich_vu,
                "thoi_gian": dv.thoi_gian_dich_vu
            }
            for dv in dich_vu_list
        ]


        return render_template('booking.html', list_services=list_services, dich_vu_list = dich_vu_list)

    # ---------- POST (JSON) ----------
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Không nhận được JSON"
        }), 400

    services = data.get('services')

    try:
        dat_lich = add_dat_lich(data)

        add_dat_lich_detail(dat_lich.id, services)

        db.session.commit()


    except Exception as ex:

        return jsonify({"status": 500, "err_msg": str(ex)})

    else:

        return jsonify({"status": 200, "sc_msg": "Đã tiếp nhận thông tin đặt lịch! VUi lòng đợi lễ tân liên hệ lại để xác nhận đặt lịch"})

@app.route('/appointments/<int:id>')
@login_required
def appointment(id):
    if current_user.role_user != UserRole.LE_TAN:
        return redirect('/')
    kw = request.args.get("search")
    status = request.args.get("status")
    if status == None:
        status = 'LE_TAN'
    page = int(request.args.get("page", id))
    pages = math.ceil(count_appointments(status=status, kw=kw) / app.config["PAGE_SIZE"])

    appointments = load_appointments(status=status, kw=kw, page=page)
    appointment_details = None
    therapists = None

    if id > 0:
        appointment_details = get_appointment_details(appointment_id=id)
        if get_appointment_status(appointment_id=id) == TrangThaiDatLich.CHO_XAC_NHAN:
            therapists = get_free_therapists_list(appointment_details=appointment_details)

    return render_template("appointments.html", pages=pages, page=page, id=id, kw=kw, status=status,
                           appointments=appointments,
                           appointment_details=appointment_details,
                           therapists=therapists)


@app.route('/appointments/<int:id>/success', methods=['POST'])
@login_required
def success_appointment(id):
    if current_user.role_user != UserRole.LE_TAN:
        return redirect('/')
    data = request.get_json()

    if not data or 'selectedTherapists' not in data:
        return jsonify({"status": 400, "err_msg": "Dữ liệu không tồn tại"})

    selected_therapists = data['selectedTherapists']

    check = assign_therapists(appointment_id=id, selected_therapists=selected_therapists)
    if check == -1:
        return jsonify({"status": 400, "err_msg": "Dữ liệu không hợp lệ"})

    add_busy_time(appointment_id=id, selected_therapists=selected_therapists)
    assign_receptionist(appointment_id=id, receptionist_id=current_user.id)
    change_appointment_status(appointment_id=id, status=TrangThaiDatLich.DA_XAC_NHAN)

    return jsonify({
        "status": 200,
    })


@app.route('/appointments/<int:id>/carryOut')
@login_required
def carry_out_appointment(id):
    if current_user.role_user != UserRole.LE_TAN:
        return redirect('/')
    change_appointment_status(appointment_id=id, status=TrangThaiDatLich.DANG_THUC_HIEN)
    return redirect('/appointments/0?status=LE_TAN&page=1')


@app.route('/appointments/<int:id>/cancel')
@login_required
def cancel_appointment(id):
    if current_user.role_user != UserRole.LE_TAN:
        return redirect('/')
    del_busy_time(appointment_id=id)
    change_appointment_status(appointment_id=id, status=TrangThaiDatLich.DA_HUY)
    return redirect('/appointments/' + str(id) + '?status=LE_TAN&page=1')


@app.route('/serviceSheets/<int:id>')
@login_required
def service_sheet(id):
    if current_user.role_user != UserRole.KY_THUAT_VIEN:
        return redirect('/')
    kw = request.args.get("search")
    status = request.args.get("status")
    hind = False

    therapist = KyThuatVien.query.get(current_user.id)
    therapist_busy_time = get_busy_time(therapist_id=therapist.user.id)
    service_now = present_service(id)
    service_next = next_service(id)

    if status == None:
        status = 'KTV'
    elif status == 'DA_XAC_NHAN':
        hind = True

    page = int(request.args.get("page", id))
    pages = math.ceil(count_appointments(status=status, kw=kw, hind=hind, appointments=therapist_busy_time) / app.config["PAGE_SIZE"])
    appointments = load_appointments(status=status, kw=kw, page=page, hind=hind, appointments=therapist_busy_time)

    service_sheet_details = None
    appointment_details = None

    if id > 0:
        if load_service_sheets(appointment_id=id):
            sheet = load_service_sheets(appointment_id=id)
            service_sheet_details = get_service_sheet_details(service_sheet_id=sheet.id)
        appointment_details = get_appointment_details(appointment_id=id)

    return render_template("serviceSheets.html", pages=pages, page=page, id=id, kw=kw, status=status,
                           service_sheet_details=service_sheet_details,
                           appointments=appointments,
                           appointment_details=appointment_details,
                           therapist_busy_time=therapist_busy_time,
                           user=therapist,
                           service_now=service_now,
                           service_next=service_next)


@app.route('/serviceSheets/update/<int:id>')
@login_required
def update_service_sheet(id):
    if current_user.role_user != UserRole.KY_THUAT_VIEN:
        return redirect('/')
    flag = True
    hind = False
    kw = request.args.get("search")
    status = request.args.get("status")

    therapist = KyThuatVien.query.get(current_user.id)
    therapist_busy_time = get_busy_time(therapist_id=therapist.user.id)
    service_now = present_service(id)
    service_next = next_service(id)

    if status == None:
        status = 'KTV'
    elif status == 'DA_XAC_NHAN':
        hind = True

    page = int(request.args.get("page", id))
    pages = math.ceil(count_appointments(status=status, kw=kw, hind=hind, appointments=therapist_busy_time) / app.config["PAGE_SIZE"])
    appointments = load_appointments(status=status, kw=kw, page=page, hind=hind, appointments=therapist_busy_time)

    appointment_details = get_appointment_details(appointment_id=id)
    service_sheet_details = None

    if load_service_sheets(appointment_id=id):
        sheet = load_service_sheets(appointment_id=id)
        service_sheet_details = get_service_sheet_details(service_sheet_id=sheet.id)

    return render_template("serviceSheets.html", pages=pages, page=page, id=id, kw=kw, status=status, flag=flag,
                           service_sheet_details=service_sheet_details,
                           appointments=appointments,
                           appointment_details=appointment_details,
                           therapist_busy_time=therapist_busy_time,
                           user=therapist,
                           service_now=service_now,
                           service_next=service_next)


@app.route('/serviceSheets/update/<int:id>/success', methods=['POST'])
@login_required
def success_service_sheet(id):
    if current_user.role_user != UserRole.KY_THUAT_VIEN:
        return redirect('/')
    data = request.get_json()
    if not data:
        return jsonify({"status": 400, "err_msg": "Dữ liệu không tồn tại"})

    update_sheet_detail(id, data)

    return jsonify({
        "status": 200,
    })


@app.route('/invoices/<int:id>')
@login_required
def invoice(id):
    if current_user.role_user != UserRole.THU_NGAN:
        return redirect('/')
    flag = False
    kw = request.args.get("search")
    page = int(request.args.get("page", id))
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

        else:
            receipt_discount = get_receipt_discount(receipt_id=receipt.id)

    return render_template("invoices.html", pages=pages, page=page, id=id, kw=kw, flag=flag,
                           service_sheets=service_sheets,
                           service_sheet_detail=service_sheet_detail,
                           receipt=receipt,
                           receipt_discount=receipt_discount,
                           invoice=invoice,
                           total_tmp=total_tmp)


@app.route('/invoices/<int:id>/add_discount', methods=['PUT'])
@login_required
def add_discount(id):
    if current_user.role_user != UserRole.THU_NGAN:
        return redirect('/')
    discount = check_discount(request.json.get("ma_giam_gia"), request.json.get("ma_khach_hang"))
    if discount == -1:
        return jsonify({"status": 400, "err_msg": "Mã giảm giá không hợp lệ"})
    elif discount == 0:
        return jsonify({"status": 400, "err_msg": "Mã giảm giá hết hạn sử dụng"})

    invoice = session.get('invoice', {})
    print(invoice)
    if invoice and str(id) in invoice and str(discount.dich_vu.id) in invoice[str(id)]:
        if invoice[str(id)][str(discount.dich_vu.id)]["ma_giam_gia"] is not None:
            return jsonify({"status": 400, "err_msg": "Mã giảm giá đang được áp dụng"})
        invoice[str(id)][str(discount.dich_vu.id)]['ma_giam_gia'] = discount.id
        invoice[str(id)][str(discount.dich_vu.id)]['muc_giam_gia'] = discount.muc_giam_gia
        session.modified = True

    else:
        return jsonify({"status": 400, "err_msg": "Mã giảm giá không hợp lệ"})

    return jsonify(utils.total(invoice=invoice[str(id)]))


@app.route('/invoices/<int:id>/remove_discount', methods=['PUT'])
@login_required
def remove_discount(id):
    if current_user.role_user != UserRole.THU_NGAN:
        return redirect('/')
    invoice = session.get('invoice', {})
    service_id = request.json.get("ma_dich_vu")

    if invoice and str(id) in invoice and str(service_id) in invoice[str(id)]:
        if invoice[str(id)][str(service_id)]["ma_giam_gia"] is None:
            return jsonify({"status": 400, "err_msg": "Dịch vụ đang không sử dụng mã giảm giá"})
        else:
            invoice[str(id)][str(service_id)]["ma_giam_gia"] = None
            invoice[str(id)][str(service_id)]["muc_giam_gia"] = 0
            session.modified = True
    else:
        return jsonify({"status": 400, "err_msg": "Lỗi hệ thống"})

    return jsonify(utils.total(invoice=invoice[str(id)]))


@app.route('/invoices/<int:id>/payment')
@login_required
def payment(id):
    if current_user.role_user != UserRole.THU_NGAN:
        return redirect('/')
    flag = True
    service_sheet_detail = get_service_sheet_details(service_sheet_id=id)
    invoice = session.get('invoice', {})
    total_tmp = utils.total(invoice=invoice[str(id)])
    return render_template("invoices.html", id=id, flag=flag,
                           service_sheet_detail=service_sheet_detail,
                           invoice=invoice,
                           total_tmp=total_tmp)


@app.route('/invoices/<int:id>/payment/success', methods=['POST'])
@login_required
def success_pay(id):
    if current_user.role_user != UserRole.THU_NGAN:
        return redirect('/')
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
                    paid=paid, sheet_id=id, cashier_id=customer_id)
    except Exception as ex:
        return jsonify({"status": 500, "err_msg": str(ex)})
    else:
        del session['invoice'][str(id)]
        session.modified = True
        return jsonify({"status": 200})


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
