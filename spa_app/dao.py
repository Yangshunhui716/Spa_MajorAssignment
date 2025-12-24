import hashlib
from datetime import datetime, time, timedelta
from sqlalchemy import case, cast, Date
from spa_app import app, db
from spa_app.models import KyThuatVien, DichVu, DatLich, PhieuDichVu, HoaDon, DatLichDetail, PhieuDichVuDetail, \
    MaGiamGia, VAT, KhachHangMaGiamGia, User, ThoiGianBieuKTV, ThoiGianKTVBan, HoaDonMaGiamGia, TrangThaiDatLich, \
    TrangThaiMaGiamGiaEnum


def auth_user(username, password):
    print("LOGIN TRY:")
    print(" - username:", repr(username))
    print(" - raw password:", repr(password))

    password = hashlib.md5(password.encode("utf-8")).hexdigest()
    print(" - hashed:", password)

    user = User.query.filter(
        User.tai_khoan_user == username,
        User.password_user == password
    ).first()

    print(" - user found:", user)
    return user


def add_user(name, username, password, email, phone):
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    u = User(ho_ten_user=name, password_user=password, sdt_user=phone, email_user=email, tai_khoan_user=username)
    db.session.add(u)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_user_by_phone(sdt_user):
    return User.query.filter_by(sdt_user=sdt_user).first()


def get_user_by_username(username):
    return User.query.filter_by(tai_khoan_user=username).first()


def is_ky_thuat_vien(user_id):
    return db.session.query(KyThuatVien) \
        .filter(KyThuatVien.ma_ktv == user_id) \
        .first()


def add_dat_lich(data_dat_lich):
    name = data_dat_lich.get('name')
    phone = data_dat_lich.get('phone')
    email = data_dat_lich.get('email')
    note = data_dat_lich.get('note')
    date = data_dat_lich.get('date')
    time = data_dat_lich.get('time')

    print(name,phone)

    gio_hen = datetime.strptime(
        f"{date} {time}", "%Y-%m-%d %H:%M"
    )

    user = User.query.filter_by(sdt_user = phone).first()

    if user:
        user.ho_ten_user = name
        user.email_user = email
    else:
        user = User(
            ho_ten_user = name,
            sdt_user = phone,
            email_user = email
        )

        db.session.add(user)
        db.session.flush()

    dat_lich = DatLich(
        ma_khach_hang = user.id,
        gio_hen = gio_hen,
        ghi_chu = note,
        thoi_gian_xu_ly = datetime.now(),
        trang_thai_dat_lich = TrangThaiDatLich.CHO_XAC_NHAN
    )


    db.session.add(dat_lich)
    db.session.flush()

    return dat_lich

def add_dat_lich_detail(ma_dat_lich, services):
    for s in services:
        detail = DatLichDetail(
            ma_dat_lich=ma_dat_lich,
            ma_dich_vu=s['id'],
        )
        db.session.add(detail)



def load_therapists(therapist_id):
    if therapist_id:
        return KyThuatVien.query.get(therapist_id)
    return KyThuatVien.query.all()


def get_free_therapists_list(appointment_details):
    appointment = appointment_details[0].dat_lich
    work_shift = work_shift_appointment(appointment.gio_hen)
    therapists_schedule = load_schedule(appointment.gio_hen, work_shift)
    therapists_list = []

    start_time = appointment.gio_hen
    for a in appointment_details:
        end_time = start_time + timedelta(minutes=a.dich_vu.thoi_gian_dich_vu)
        for t in therapists_schedule:
            if (a.ma_dich_vu == t.ky_thuat_vien.dich_vu.id):
                if (busy_time(t.ma_ky_thuat_vien) < a.dich_vu.gioi_han_khach):
                    if (busy_time(t.ma_ky_thuat_vien, start_time, end_time) == None):
                        therapists_list.append(t.ky_thuat_vien)
        start_time = end_time

    return therapists_list


def busy_time(therapist_id, start_time=None, end_time=None):
    if start_time and end_time:
        return ThoiGianKTVBan.query.filter(ThoiGianKTVBan.ma_ky_thuat_vien == therapist_id,
                                           start_time < (ThoiGianKTVBan.thoi_gian_ket_thuc),
                                           end_time > ThoiGianKTVBan.thoi_gian_bat_dau).first()
    return ThoiGianKTVBan.query.filter(ThoiGianKTVBan.ma_ky_thuat_vien == therapist_id).count()


def work_shift_appointment(appointment_time):
    t = appointment_time.time()
    if time(8, 0) <= t < time(12, 0):
        return "S"
    if time(12, 0) <= t < time(17, 0):
        return "C"
    if time(17, 0) <= t < time(20, 0):
        return "T"
    return None


def load_schedule(customer_date, work_shift):
    thu_map = {
        1: "t2",
        2: "t3",
        3: "t4",
        4: "t5",
        5: "t6",
        6: "t7",
        7: "cn"
    }
    shift_compatible = {
        "S": ["S", "A"],
        "C": ["C", "A", "B"],
        "T": ["T", "B"]
    }

    thu_col = getattr(ThoiGianBieuKTV, thu_map[customer_date.isoweekday()])
    allowed_shifts = shift_compatible.get(work_shift, [])

    return ThoiGianBieuKTV.query.filter(thu_col.in_(allowed_shifts)).all()


def load_services():
    return DichVu.query.all()


def load_appointments(appointment_id=None, status=None, kw=None, page=None, hind=False):
    query = DatLich.query
    if kw:
        query = query.filter(DatLich.khach_hang.has(User.ho_ten_user.ilike(f"%{kw}%")))

    if appointment_id:
        return query.get(appointment_id)

    match status:
        case "CHO_XAC_NHAN":
            query = (query.filter(DatLich.trang_thai_dat_lich == "CHO_XAC_NHAN")
                     .order_by(DatLich.ngay_tao.asc(), DatLich.gio_hen.asc()))
        case "DA_XAC_NHAN":
            if hind == True:
                query = query.filter(DatLich.trang_thai_dat_lich == "DA_XAC_NHAN",
                                     cast(DatLich.gio_hen, Date) == datetime.now().date()).order_by(
                    DatLich.gio_hen.asc())
            else:
                query = (query.filter(DatLich.trang_thai_dat_lich == "DA_XAC_NHAN")
                         .order_by(case((cast(DatLich.gio_hen, Date) == datetime.now().date(), 0), else_=1)
                                   , DatLich.gio_hen.desc()))
        case "DANG_THUC_HIEN":
            query = (query.filter(DatLich.trang_thai_dat_lich == "DANG_THUC_HIEN")
                     .order_by(DatLich.gio_hen.asc()))
        case "DA_HOAN_THANH":
            query = (query.filter(DatLich.trang_thai_dat_lich == "DA_HOAN_THANH",
                                  cast(DatLich.gio_hen, Date) == datetime.now().date())
                     .order_by(DatLich.gio_hen.desc()))
        case "DA_HUY":
            query = (query.filter(DatLich.trang_thai_dat_lich == "DA_HUY")
                     .order_by(DatLich.gio_hen.desc()))
        case "LE_TAN":
            query = query.filter(DatLich.trang_thai_dat_lich.in_([
                "CHO_XAC_NHAN",
                "DA_XAC_NHAN",
                "DA_HUY"
            ])).order_by(
                case((DatLich.trang_thai_dat_lich == "CHO_XAC_NHAN", 1),
                     (DatLich.trang_thai_dat_lich == "DA_XAC_NHAN", 2),
                     (DatLich.trang_thai_dat_lich == "DA_HUY", 3),
                     else_=4
                     ), DatLich.gio_hen.asc())
        case "KTV":
            query = query.filter(DatLich.trang_thai_dat_lich.in_([
                "DA_XAC_NHAN",
                "DANG_THUC_HIEN",
                "DA_HOAN_THANH"
            ]), cast(DatLich.gio_hen, Date) == datetime.now().date()).order_by(
                case((DatLich.trang_thai_dat_lich == "DANG_THUC_HIEN", 1),
                     (DatLich.trang_thai_dat_lich == "DA_XAC_NHAN", 2),
                     (DatLich.trang_thai_dat_lich == "DA_HOAN_THANH", 3),
                     else_=4
                     ), DatLich.gio_hen.asc())

    if page:
        size = app.config["PAGE_SIZE"]
        start = (int(page) - 1) * size
        query = query.slice(start, start + size)

    return query.all()


def count_appointments(status=None, kw=None, hind=False):
    query = DatLich.query
    if kw:
        query = query.filter(DatLich.khach_hang.has(User.ho_ten_user.ilike(f"%{kw}%")))

    match status:
        case "CHO_XAC_NHAN":
            query = query.filter(DatLich.trang_thai_dat_lich == "CHO_XAC_NHAN")
        case "DA_XAC_NHAN":
            if hind == True:
                query = query.filter(DatLich.trang_thai_dat_lich == "DA_XAC_NHAN",
                                     cast(DatLich.gio_hen, Date) == datetime.now().date())
            else:
                query = query.filter(DatLich.trang_thai_dat_lich == "DA_XAC_NHAN")
        case "DANG_THUC_HIEN":
            query = query.filter(DatLich.trang_thai_dat_lich == "DANG_THUC_HIEN")
        case "DA_HOAN_THANH":
            query = query.filter(DatLich.trang_thai_dat_lich == "DA_HOAN_THANH",
                                 cast(DatLich.gio_hen, Date) == datetime.now().date())
        case "DA_HUY":
            query = query.filter(DatLich.trang_thai_dat_lich == "DA_HUY")
        case "LE_TAN":
            query = query.filter(DatLich.trang_thai_dat_lich.in_([
                "CHO_XAC_NHAN",
                "DA_XAC_NHAN",
                "DA_HUY"
            ]))
        case "KTV":
            query = query.filter(DatLich.trang_thai_dat_lich.in_([
                "DA_XAC_NHAN",
                "DANG_THUC_HIEN",
                "DA_HOAN_THANH"
            ]), cast(DatLich.gio_hen, Date) == datetime.now().date())

    return query.count()


def get_appointment_details(appointment_id):
    return DatLichDetail.query.filter(DatLichDetail.ma_dat_lich == appointment_id).all()


def get_appointment_status(appointment_id):
    a = load_appointments(appointment_id=appointment_id)
    return a.trang_thai_dat_lich


def change_appointment_status(appointment_id, status):
    a = load_appointments(appointment_id=appointment_id)
    a.trang_thai_dat_lich = status
    db.session.commit()


def assign_receptionist(appointment_id, receptionist_id):
    a = load_appointments(appointment_id=appointment_id)
    a.ma_le_tan = receptionist_id
    a.thoi_gian_xu_ly = datetime.now()
    db.session.commit()


def assign_therapists(appointment_id, selected_therapists):
    details = get_appointment_details(appointment_id)
    if len(details) != len(selected_therapists):
        return -1
    for detail, th in zip(details, selected_therapists):
        detail.ma_ky_thuat_vien = int(th["ma_ktv"])
    db.session.commit()
    return 1


def add_busy_time(appointment_id, selected_therapists):
    a = load_appointments(appointment_id=appointment_id)
    start_time = a.gio_hen
    for th in selected_therapists:
        therapist = load_therapists(therapist_id=th["ma_ktv"])
        end_time = start_time + timedelta(
            minutes=therapist.dich_vu.thoi_gian_dich_vu + therapist.dich_vu.thoi_gian_nghi_ngoi)
        busy = ThoiGianKTVBan(ma_ky_thuat_vien=therapist.user.id, ma_dat_lich=a.id,
                              thoi_gian_bat_dau=start_time, thoi_gian_ket_thuc=end_time)
        db.session.add(busy)
        start_time = end_time - timedelta(minutes=therapist.dich_vu.thoi_gian_nghi_ngoi)
    db.session.commit()


def del_busy_time(appointment_id):
    ThoiGianKTVBan.query.filter(ThoiGianKTVBan.ma_dat_lich == appointment_id).delete()
    db.session.commit()


def load_service_sheets(appointment_id=None, sheet_id=None, kw=None, page=None, flag=True):
    query = PhieuDichVu.query.join(DatLich)

    if kw:
        query = query.join(User).filter(User.ho_ten_user.ilike(f"%{kw}%"))

    if appointment_id:
        return query.filter(PhieuDichVu.ma_dat_lich == appointment_id).first()

    if sheet_id:
        return query.filter(PhieuDichVu.id == sheet_id).first()

    if flag is False:
        query = (query.filter(DatLich.trang_thai_dat_lich.in_([
            "DANG_THUC_HIEN",
            "DA_HOAN_THANH"
        ]), cast(DatLich.gio_hen, Date) == datetime.now().date()).order_by(
            case((DatLich.trang_thai_dat_lich == "DA_THUC_HIEN", 1),
                 (DatLich.trang_thai_dat_lich == "DA_HOAN_THANH", 2), else_=3),
            DatLich.gio_hen.asc()))

    if page:
        size = app.config["PAGE_SIZE"]
        start = (int(page) - 1) * size
        query = query.slice(start, start + size)

    return query.all()


def count_service_sheets(kw=None, flag=True):
    query = PhieuDichVu.query.join(DatLich)

    if kw:
        query = query.join(User).filter(User.ho_ten_user.ilike(f"%{kw}%"))

    if flag is False:
        query = (query.filter(DatLich.trang_thai_dat_lich.in_([
            "DANG_THUC_HIEN",
            "DA_HOAN_THANH"
        ]), cast(DatLich.gio_hen, Date) == datetime.now().date()))

    return query.count()


def get_service_sheet_details(service_sheet_id, service_id=None):
    if service_id:
        return PhieuDichVuDetail.query.filter(PhieuDichVuDetail.ma_phieu_dich_vu == service_sheet_id,
                                              PhieuDichVuDetail.ma_dich_vu == service_id).first()
    return PhieuDichVuDetail.query.filter(PhieuDichVuDetail.ma_phieu_dich_vu == service_sheet_id).all()


def update_sheet_detail(appointment_id, update_content):
    service_sheet = load_service_sheets(appointment_id=appointment_id)
    if service_sheet is None:
        service_sheet = PhieuDichVu(ma_dat_lich=appointment_id, ngay_tao=datetime.now())
        db.session.add(service_sheet)
        db.session.commit()

        for detail in get_appointment_details(appointment_id):
            if (detail.ma_dich_vu == update_content["ma_dich_vu"]):
                sheet_detail = PhieuDichVuDetail(ma_phieu_dich_vu=service_sheet.id,
                                                 ma_dich_vu=update_content["ma_dich_vu"]
                                                 , thoi_gian_cap_nhat=datetime.now(),
                                                 ghi_chu_ktv=update_content["ghi_chu"]
                                                 , phan_hoi_khach_hang=update_content["phan_hoi"])
            else:
                sheet_detail = PhieuDichVuDetail(ma_phieu_dich_vu=service_sheet.id, ma_dich_vu=detail.ma_dich_vu
                                                 , thoi_gian_cap_nhat=None, ghi_chu_ktv=None
                                                 , phan_hoi_khach_hang=None)
            db.session.add(sheet_detail)
            db.session.commit()
    else:
        sheet_detail = get_service_sheet_details(service_sheet.id, update_content["ma_dich_vu"])
        sheet_detail.ghi_chu_ktv = update_content["ghi_chu"]
        sheet_detail.phan_hoi_khach_hang = update_content["phan_hoi"]
        sheet_detail.thoi_gian_cap_nhat = datetime.now()
        db.session.commit()


def load_discounts(discount_id=None):
    if discount_id:
        return MaGiamGia.query.filter(MaGiamGia.id == discount_id).first()
    return MaGiamGia.query.all()


def get_customer_discount(customer_id=None, discount_id=None):
    query = KhachHangMaGiamGia.query

    if customer_id:
        query = query.filter(KhachHangMaGiamGia.ma_khach_hang == customer_id)

    if discount_id:
        query = query.filter(KhachHangMaGiamGia.ma_giam_gia == discount_id)

    return query.first()


def check_discount(discount_id, customer_id):
    discount = load_discounts(discount_id=discount_id)
    if discount is None:
        return -1

    if discount.ngay_het_han < datetime.now():
        return 0

    customer_discount = get_customer_discount(customer_id=customer_id, discount_id=discount_id)
    if customer_discount is None or customer_discount.trang_thai == TrangThaiMaGiamGiaEnum.DA_SU_DUNG:
        return -1

    return discount


def get_vat():
    return VAT.query.order_by(VAT.ngay_tao.desc()).first()


def get_receipt(service_sheet_id):
    return HoaDon.query.filter(HoaDon.ma_phieu_dich_vu == service_sheet_id).first()


def add_receipt(customer_id, invoice, sheet_id, cashier_id, payment_method, temporary, total_discount, total_amount,
                paid):
    receipt = HoaDon(ma_thu_ngan=cashier_id, ma_phieu_dich_vu=sheet_id,
                     ma_vat=get_vat().id, phuong_thuc_thanh_toan=payment_method,
                     tong_gia_dich_vu=temporary, tong_giam_gia=total_discount,
                     tong_thanh_toan=total_amount, so_tien_nhan=paid,
                     thoi_gian_thanh_toan=datetime.now())
    db.session.add(receipt)
    db.session.flush()

    for i in invoice.values():
        if i.get('ma_giam_gia') is not None:
            receipt_discount = HoaDonMaGiamGia(ma_hoa_don=receipt.id, ma_giam_gia=i.get('ma_giam_gia'))
            db.session.add(receipt_discount)
            customer_discount = get_customer_discount(customer_id=customer_id, discount_id=i.get("ma_giam_gia"))
            customer_discount.trang_thai = TrangThaiMaGiamGiaEnum.DA_SU_DUNG

    service_sheet = load_service_sheets(sheet_id=sheet_id)
    change_appointment_status(appointment_id=service_sheet.dat_lich.id, status=TrangThaiDatLich.DA_HOAN_THANH)

    db.session.commit()


def get_receipt_discount(receipt_id):
    return HoaDonMaGiamGia.query.filter(HoaDonMaGiamGia.ma_hoa_don == receipt_id).all()
