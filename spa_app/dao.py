import json
from datetime import datetime

from sqlalchemy import false

from spa_app import app, db
from spa_app.models import KyThuatVien, DichVu, DatLich, PhieuDichVu, HoaDon, DatLichDetail, PhieuDichVuDetail

def load_therapists():
    return KyThuatVien.query.all()

def load_services():
    return DichVu.query.all()

def load_appointments():
    return DatLich.query.all()

def get_appointment_details(appointment_id):
    return DatLichDetail.query.filter(DatLichDetail.ma_dat_lich == appointment_id).all()

def change_appointment_status(appointment_id, status):
    ad = DatLich.query.get(appointment_id)
    ad.trang_thai_dat_lich = status
    db.session.commit()

def assign_therapists(appointment_id, selected_therapists):
    details = get_appointment_details(appointment_id)
    if len(details) != len(selected_therapists):
        return -1
    for detail, th in zip(details, selected_therapists):
        detail.ma_ky_thuat_vien= int(th["ma_ktv"])
    db.session.commit()
    return 1

def load_service_sheets(appointment_id=None):
    if id:
        return PhieuDichVu.query.get(appointment_id)
    return PhieuDichVu.query.all()

def get_service_sheet_details(service_sheet_id, service_id=None):
    print(service_sheet_id)
    print(service_id)
    if service_id:
        return PhieuDichVuDetail.query.filter(PhieuDichVuDetail.ma_phieu_dich_vu == service_sheet_id, PhieuDichVuDetail.ma_dich_vu==service_id).first()
    return PhieuDichVuDetail.query.filter(PhieuDichVuDetail.ma_phieu_dich_vu == service_sheet_id).all()

def update_sheet_detail(appointment_id, update_content):
    service_sheet = load_service_sheets(appointment_id)
    if service_sheet == None:
        service_sheet = PhieuDichVu(ma_dat_lich=appointment_id, ngay_tao=datetime.now())
        db.session.add(service_sheet)
        db.session.commit()
        sheet_detail = PhieuDichVuDetail(ma_phieu_dich_vu=service_sheet.id, ma_dich_vu=update_content["ma_dich_vu"]
                                         , thoi_gian_cap_nhat=datetime.now(), ghi_chu_ktv=update_content["ghi_chu"]
                                         , phan_hoi_khach_hang=update_content["phan_hoi"])
        db.session.add(sheet_detail)
        db.session.commit()
    else:
        sheet_detail = get_service_sheet_details(service_sheet.id, update_content["ma_dich_vu"])
        sheet_detail.ghi_chu_ktv = update_content["ghi_chu"]
        sheet_detail.phan_hoi_khach_hang=update_content["phan_hoi"]
        sheet_detail.thoi_gian_cap_nhat=datetime.now()
        db.session.commit()






