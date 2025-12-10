import datetime

from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime, Enum, Double
from spa_app import db,app
from enum import Enum as RoleEnum

class UserRole(RoleEnum):
    USER = "USER"
    KHACH_HANG = "Khach_Hang"
    LE_TAN = "Le_Tan"
    THU_NGAN = "Thu_Ngan"
    QUAN_LY = "Quan_LY"
    QUAN_TRI_VIEN ="Quan_Tri_Vien"

class TrangThaiKTV(RoleEnum):
    RANH = 'RANH'
    BAN = 'BAN'
    DANG_PHUC_VU = "DANG_PHUC_VU"
    NGHI = 'NGHI'

class TrangThaiDatLich(RoleEnum):
    DA_HOAN_THANH = "DA_HOAN_THANH"
    DA_HUY = "DA_HUY"
    DA_XAC_NHAN = "DA_XAC_NHAN"
    CHO_XAC_NHAN = "CHO_XAC_NHAN"
    DANG_THUC_HIEN ="DANG_THUC_HIEN"

class CaLamEnum(RoleEnum):
    NONE ="NONE"
    S = "8:00 - 11:59"
    C = "12:00 - 15:59"
    T = "17:00 - 20:00"
    A = "8:00 - 13:50"
    B = "14:00 - 20:00"

class TrangThaiMaGiamGiaEnum(RoleEnum):
    DA_SU_DUNG = "DA_SU_DUNG"
    CHUA_SU_DUNG="CHUA_SU_DUNG"
    DA_HET_HAN = "DA_HET_HAN"

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True,unique=True)
    ngayTao=Column(DateTime,nullable=False)

class User(BaseModel):
    hoTenUser = Column(String(150), nullable=False)
    sdtUser = Column(Integer,nullable=False,unique=True)
    emailUser = Column(String(150),nullable=False)
    taiKhoanUser = Column(String(50),nullable=False)
    passwordUser = Column(String(50),nullable=False)
    roleUser = Column(Enum(UserRole),nullable=False,default=UserRole.USER)

class DichVu(BaseModel):
    tenDichVu = Column(String(150),nullable=False,unique=True)
    giaDichVu = Column(Double,nullable=False,default=0)
    thoiGianDichVu = Column(Integer,nullable=False,default=0)

class DatLich(BaseModel):
    trangThaiDatLich = Column(Enum(TrangThaiDatLich),nullable=False,default=TrangThaiDatLich.CHO_XAC_NHAN)
    #khach hang datlich
    maKhachHang = Column(Integer,ForeignKey(User.id,ondelete='CASCADE'),nullable=False)
    #le tan xu ly don dat lich
    maLeTan = Column(Integer,ForeignKey(User.id,ondelete='CASCADE'),nullable=False)


class KyThuatVien(User):
    soLuongKhach = Column(Integer,nullable=False,default=0)
    gioiHanKhach = Column(Integer,nullable=False,default=5)
    trangThai = Column(Enum(TrangThaiKTV),nullable=False, default=TrangThaiKTV.RANH)
    dichVuChuyeMon = Column(Integer,ForeignKey(DichVu.id),nullable=False)

class ThoiGianBieuKTV(db.Model):
    maKyThuatVien = Column(Integer,ForeignKey(KyThuatVien.id,ondelete='CASCADE'),primary_key=True)
    T2 = Column(Enum(CaLamEnum),nullable=False, default=CaLamEnum.NONE)
    T3 = Column(Enum(CaLamEnum),nullable=False, default=CaLamEnum.NONE)
    T4 = Column(Enum(CaLamEnum),nullable=False, default=CaLamEnum.NONE)
    T5 = Column(Enum(CaLamEnum),nullable=False, default=CaLamEnum.NONE)
    T6 = Column(Enum(CaLamEnum),nullable=False, default=CaLamEnum.NONE)
    T7 = Column(Enum(CaLamEnum),nullable=False, default=CaLamEnum.NONE)
    CN = Column(Enum(CaLamEnum),nullable=False, default=CaLamEnum.NONE)

class ThoiGianKTVBan(db.Model):
    maKyThuatVien = Column(Integer,ForeignKey(KyThuatVien.id,ondelete='CASCADE'),primary_key=True)
    thoiGianBatDau = Column(DateTime,nullable=False)
    thoiGianKetThuc = Column(DateTime,nullable=False)


class DatLichDetail(BaseModel):

    maDatLich = Column(Integer,ForeignKey(DatLich.id,ondelete='CASCADE'),nullable=False)
    maDichVu = Column(Integer,ForeignKey(DichVu.id,ondelete='CASCADE'),nullable=False)
    maKyThuatVien = Column(Integer,ForeignKey(KyThuatVien.id,ondelete='CASCADE'),nullable=False)

class PhieuDichVu(BaseModel):
    maDatLich = Column(Integer,ForeignKey(DatLich.id,ondelete='CASCADE'),nullable=False)

class PhieuDichVuDetail(BaseModel):
    maPhieuDichVu = Column(Integer,ForeignKey(PhieuDichVu.id,ondelete='CASCADE'),nullable=False)
    maDichVu = Column(Integer,ForeignKey(DichVu.id,ondelete='CASCADE'),nullable=False)
    thoiLuongThucTe = Column(Integer,nullable=False,default=0)
    ghiChuKtv = Column(Text,default="")
    phanHoiKhachHang = Column(Text,default="")


class VAT(BaseModel):
    mucVat = Column(Double,nullable=False,default=0.08)

class MaGiamGia(BaseModel):
    tenMaGiamGia = Column(String(150),nullable=False,unique=True)
    mucGiamGia = Column(Double,nullable=False,default=0)

class HoaDon(BaseModel):
    maPhieuDichVu = Column(Integer,ForeignKey(PhieuDichVu.id,ondelete='CASCADE'),nullable=False)
    maVat = Column(Integer,ForeignKey(VAT.id),nullable=False)
    maGiamGia = Column(Integer,ForeignKey(MaGiamGia.id),nullable=False)
    tongGiaDichVu = Column(Double,nullable=False, default=0)
    tongThanhToan = Column(Double,nullable=False,default=0)

class KhachHangMaGiamGia(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    maGiamGia = Column(Integer,ForeignKey(MaGiamGia.id,ondelete='CASCADE'),nullable=False)
    maKhachHang=Column(Integer,ForeignKey(User.id,ondelete='CASCADE'),nullable=False)
    ngayBatDau= Column(DateTime,nullable=False)
    ngayHetHan = Column(DateTime,nullable=False,)
    trangThai= Column(Enum(TrangThaiMaGiamGiaEnum), nullable= False, default=TrangThaiMaGiamGiaEnum.CHUA_SU_DUNG)

if __name__ =="__main__":
    with app.app_context():
        db.create_all()



