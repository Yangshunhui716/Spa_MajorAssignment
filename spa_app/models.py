from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime, Enum, Double
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from spa_app import db, app
from enum import Enum as RoleEnum

class UserRole(RoleEnum):
    USER = "USER"
    KHACH_HANG = "Khach_Hang"
    LE_TAN = "Le_Tan"
    THU_NGAN = "Thu_Ngan"
    QUAN_LY = "Quan_Ly"
    QUAN_TRI_VIEN = "Quan_Tri_Vien"


class TrangThaiDatLich(RoleEnum):
    DA_HOAN_THANH = "DA_HOAN_THANH"
    DA_HUY = "DA_HUY"
    DA_XAC_NHAN = "DA_XAC_NHAN"
    CHO_XAC_NHAN = "CHO_XAC_NHAN"
    DANG_THUC_HIEN = "DANG_THUC_HIEN"


class CaLamEnum(RoleEnum):
    NONE = "NONE"
    S = "8:00 - 11:59"
    C = "12:00 - 16:59"
    T = "17:00 - 20:00"
    A = "8:00 - 13:59"
    B = "14:00 - 20:00"


class TrangThaiMaGiamGiaEnum(RoleEnum):
    DA_SU_DUNG = "DA_SU_DUNG"
    CHUA_SU_DUNG = "CHUA_SU_DUNG"
    DA_HET_HAN = "DA_HET_HAN"


class PhuongThucThanhToanEnum(RoleEnum):
    TIEN_MAT = "TIEN_MAT"
    CHUYEN_KHOAN = "CHUYEN_KHOAN"


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    ngay_tao = Column(DateTime, nullable=False, default=datetime.now)


class User(UserMixin, BaseModel ):
    ho_ten_user = Column(String(150), nullable=False)
    sdt_user = Column(Integer, nullable=False, unique=True)
    email_user = Column(String(150), nullable=False)
    tai_khoan_user = Column(String(50), unique=True)
    password_user = Column(String(50))
    role_user = Column(Enum(UserRole), nullable=False, default=UserRole.USER)

    dat_lich_khach_hang = relationship(
        "DatLich",
        foreign_keys="DatLich.ma_khach_hang",
        backref="khach_hang",
        lazy=True
    )

    user_ky_thuat_vien = relationship("KyThuatVien", backref="user", lazy=True)

    dat_lich_le_tan = relationship(
        "DatLich",
        foreign_keys="DatLich.ma_le_tan",
        backref="le_tan",
        lazy=True
    )

class DichVu(BaseModel):
    ten_dich_vu = Column(String(150), nullable=False, unique=True)
    mo_ta = Column(String(150))
    gia_dich_vu = Column(Double, nullable=False, default=0)
    thoi_gian_dich_vu = Column(Integer, nullable=False, default=0)
    thoi_gian_nghi_ngoi = Column(Integer, nullable=False, default=0)
    gioi_han_khach = Column(Integer, nullable=False, default=5)

    phieu_dich_vu_detail = relationship("PhieuDichVuDetail", backref="dich_vu", lazy=True)
    dat_lich_detail = relationship("DatLichDetail", backref="dich_vu", lazy=True)
    ma_giam_gia = relationship("MaGiamGia", backref="dich_vu", lazy=True)
    ky_thuat_vien = relationship("KyThuatVien", backref="dich_vu", lazy=True)

class KyThuatVien(db.Model):
    ma_ktv = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'), primary_key=True, nullable=False)
    so_luong_khach = Column(Integer, nullable=False, default=0)
    dich_vu_chuyen_mon = Column(Integer, ForeignKey(DichVu.id), nullable=False)

    dat_lich_detail = relationship("DatLichDetail", backref="ky_thuat_vien", lazy=True)
    thoi_gian_bieu = relationship("ThoiGianBieuKTV", backref="ky_thuat_vien", lazy=True)

class DatLich(BaseModel):
    trang_thai_dat_lich = Column(Enum(TrangThaiDatLich), nullable=False, default=TrangThaiDatLich.CHO_XAC_NHAN)
    ma_khach_hang = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    ma_le_tan = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'))
    gio_hen = Column(DateTime, nullable=False, default=datetime.now)
    ghi_chu = Column(Text, default="")
    thoi_gian_xu_ly = Column(DateTime, nullable=False, default=datetime.now)

    phieu_dich_vu = relationship("PhieuDichVu", backref="dat_lich", lazy=True)
    dat_lich_detail = relationship("DatLichDetail", backref="dat_lich", lazy=True)


class ThoiGianBieuKTV(db.Model):
    ma_ky_thuat_vien = Column(Integer, ForeignKey(KyThuatVien.ma_ktv, ondelete='CASCADE'), primary_key=True)
    t2 = Column(Enum(CaLamEnum), nullable=False, default=CaLamEnum.NONE)
    t3 = Column(Enum(CaLamEnum), nullable=False, default=CaLamEnum.NONE)
    t4 = Column(Enum(CaLamEnum), nullable=False, default=CaLamEnum.NONE)
    t5 = Column(Enum(CaLamEnum), nullable=False, default=CaLamEnum.NONE)
    t6 = Column(Enum(CaLamEnum), nullable=False, default=CaLamEnum.NONE)
    t7 = Column(Enum(CaLamEnum), nullable=False, default=CaLamEnum.NONE)
    cn = Column(Enum(CaLamEnum), nullable=False, default=CaLamEnum.NONE)


class ThoiGianKTVBan(db.Model):
    ma_thoi_gian_ban = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    ma_ky_thuat_vien = Column(Integer, ForeignKey(KyThuatVien.ma_ktv, ondelete='CASCADE'))
    ma_dat_lich = Column(Integer, ForeignKey(DatLich.id, ondelete='CASCADE'), nullable=False)
    thoi_gian_bat_dau = Column(DateTime, nullable=False)
    thoi_gian_ket_thuc = Column(DateTime, nullable=False)


class DatLichDetail(db.Model):
    ma_dat_lich = Column(Integer, ForeignKey(DatLich.id, ondelete='CASCADE'), primary_key=True, nullable=False)
    ma_dich_vu = Column(Integer, ForeignKey(DichVu.id, ondelete='CASCADE'), primary_key=True, nullable=False)
    ma_ky_thuat_vien = Column(Integer, ForeignKey(KyThuatVien.ma_ktv, ondelete='CASCADE'))


class PhieuDichVu(BaseModel):
    ma_dat_lich = Column(Integer, ForeignKey(DatLich.id, ondelete='CASCADE'), nullable=False)

    hoa_don = relationship("HoaDon", backref="phieu_dich_vu", lazy=True)
    phieu_dich_vu_details = relationship("PhieuDichVuDetail", backref="phieu_dich_vu", lazy=True)


class PhieuDichVuDetail(db.Model):
    ma_phieu_dich_vu = Column(Integer, ForeignKey(PhieuDichVu.id, ondelete='CASCADE'), primary_key=True, nullable=False)
    ma_dich_vu = Column(Integer, ForeignKey(DichVu.id, ondelete='CASCADE'), primary_key=True, nullable=False)
    thoi_gian_cap_nhat = Column(DateTime)
    ghi_chu_ktv = Column(Text, default="")
    phan_hoi_khach_hang = Column(Text, default="")


class VAT(BaseModel):
    muc_vat = Column(Double, nullable=False, default=0.08)

    hoa_don= relationship("HoaDon", backref="vat", lazy=True)


class MaGiamGia(BaseModel):
    ten_ma_giam_gia = Column(String(150), nullable=False, unique=True)
    mo_ta = Column(String(150), default=None)
    muc_giam_gia = Column(Double, nullable=False, default=0)
    ngay_bat_dau = Column(DateTime, nullable=False)
    ngay_het_han = Column(DateTime, nullable=False)
    ma_dich_vu = Column(Integer, ForeignKey(DichVu.id, ondelete='CASCADE'), nullable=False)

    hoa_don_ma_giam_gia = relationship("HoaDonMaGiamGia", backref="giam_gia", lazy=True)


class KhachHangMaGiamGia(db.Model):
    ma_giam_gia = Column(Integer, ForeignKey(MaGiamGia.id, ondelete='CASCADE'), primary_key=True, nullable=False)
    ma_khach_hang = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'), primary_key=True, nullable=False)
    trang_thai = Column(Enum(TrangThaiMaGiamGiaEnum), nullable=False, default=TrangThaiMaGiamGiaEnum.CHUA_SU_DUNG)


class HoaDon(BaseModel):
    ma_thu_ngan = Column(Integer, ForeignKey(User.id), nullable=False)
    ma_phieu_dich_vu = Column(Integer, ForeignKey(PhieuDichVu.id, ondelete='CASCADE'), nullable=False)
    ma_vat = Column(Integer, ForeignKey(VAT.id), nullable=False)
    tong_gia_dich_vu = Column(Double, nullable=False, default=0)
    tong_giam_gia = Column(Double, nullable=False, default=0)
    tong_thanh_toan = Column(Double, nullable=False, default=0)
    so_tien_nhan = Column(Double, nullable=False, default=0)
    phuong_thuc_thanh_toan = Column(Enum(PhuongThucThanhToanEnum), nullable=False, default=PhuongThucThanhToanEnum.TIEN_MAT)
    thoi_gian_thanh_toan = Column(DateTime, nullable=False)


class HoaDonMaGiamGia(db.Model):
    ma_hoa_don = Column(Integer, ForeignKey(HoaDon.id, ondelete='CASCADE'), primary_key=True, nullable=False)
    ma_giam_gia = Column(Integer, ForeignKey(MaGiamGia.id), primary_key=True, nullable=False)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
