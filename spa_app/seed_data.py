from datetime import datetime, timedelta
from spa_app import db, app
from spa_app.models import *
from sqlalchemy import delete

def seed_data_ro_rang():
    # ================= XÓA DỮ LIỆU CŨ =================
    db.session.execute(delete(HoaDon))
    db.session.execute(delete(PhieuDichVuDetail))
    db.session.execute(delete(PhieuDichVu))
    db.session.execute(delete(DatLichDetail))
    db.session.execute(delete(DatLich))
    db.session.execute(delete(ThoiGianKTVBan))
    db.session.execute(delete(ThoiGianBieuKTV))
    db.session.execute(delete(KyThuatVien))
    db.session.execute(delete(MaGiamGia))
    db.session.execute(delete(KhachHangMaGiamGia))
    db.session.execute(delete(VAT))
    db.session.execute(delete(DichVu))
    db.session.execute(delete(User))

    db.session.commit()

    print(app.config["SQLALCHEMY_DATABASE_URI"])

    # ================= USER =================
    khach_hang_nguyen_van_a = User(
        ho_ten_user="Nguyễn Văn A",
        sdt_user=901111111,
        email_user="nguyenvana@gmail.com",
        tai_khoan_user="khach_nguyenvana",
        password_user="123456",
        role_user=UserRole.KHACH_HANG
    )

    khach_hang_nguyen_van_hoang = User(
        ho_ten_user="Nguyễn Văn Hoàng",
        sdt_user=901111112,
        email_user="nguyenvanhoang@gmail.com",
        tai_khoan_user="khach_nguyenvanhoang",
        password_user="123456",
        role_user=UserRole.KHACH_HANG
    )

    khach_hang_nguyen_van_tien = User(
        ho_ten_user="Nguyễn Văn Tiến",
        sdt_user=901111113,
        email_user="nguyenvantien@gmail.com",
        tai_khoan_user="khach_nguyenvantien",
        password_user="123456",
        role_user=UserRole.KHACH_HANG
    )

    khach_hang_tran_thi_b = User(
        ho_ten_user="Trần Thị B",
        sdt_user=902222232,
        email_user="tranthib@gmail.com",
        tai_khoan_user="khach_tranthib",
        password_user="123456",
        role_user=UserRole.KHACH_HANG
    )

    le_tan_le_thi_c = User(
        ho_ten_user="Lê Thị C",
        sdt_user=903323333,
        email_user="letan1@gmail.com",
        tai_khoan_user="le_tan1",
        password_user="123456",
        role_user=UserRole.LE_TAN
    )

    thu_ngan_pham_van_d = User(
        ho_ten_user="Phạm Văn D",
        sdt_user=904434444,
        email_user="thungan1@gmail.com",
        tai_khoan_user="thu_ngan1",
        password_user="123456",
        role_user=UserRole.THU_NGAN
    )

    user_ktv_massage_tran_gia_huy = User(
        ho_ten_user="Trần Gia Huy",
        sdt_user=905555535,
        email_user="ktv_massage1@gmail.com",
        tai_khoan_user="ktv_massage1",
        password_user="123456",
        role_user=UserRole.USER
    )

    user_ktv_massage_nguyen_quoc_huy = User(
        ho_ten_user="Nguyễn Quốc Huy",
        sdt_user=905551155,
        email_user="ktv_massage2@gmail.com",
        tai_khoan_user="ktv_massage2",
        password_user="123456",
        role_user=UserRole.USER
    )

    user_ktv_cham_soc_da_le_quang_an = User(
        ho_ten_user="Lê Quang An",
        sdt_user=906116666,
        email_user="ktv_da1@gmail.com",
        tai_khoan_user="ktv_da1",
        password_user="123456",
        role_user=UserRole.USER
    )

    user_ktv_cham_soc_da_nguyen_minh_anh = User(
        ho_ten_user="Nguyễn Minh Anh",
        sdt_user=906666966,
        email_user="ktv_da2@gmail.com",
        tai_khoan_user="ktv_da2",
        password_user="123456",
        role_user=UserRole.USER
    )

    user_ktv_goi_dau_tran_cuc = User(
        ho_ten_user="Trần Cúc",
        sdt_user=906660666,
        email_user="ktv_da2@gmail.com",
        tai_khoan_user="ktv_da2",
        password_user="123456",
        role_user=UserRole.USER
    )

    db.session.add_all([
        khach_hang_nguyen_van_a,
        khach_hang_nguyen_van_hoang,
        khach_hang_nguyen_van_tien,
        khach_hang_tran_thi_b,
        le_tan_le_thi_c,
        thu_ngan_pham_van_d,
        user_ktv_massage_tran_gia_huy,
        user_ktv_massage_nguyen_quoc_huy,
        user_ktv_cham_soc_da_le_quang_an,
        user_ktv_cham_soc_da_nguyen_minh_anh,
        user_ktv_goi_dau_tran_cuc
    ])
    db.session.commit()

    # ================= DỊCH VỤ =================
    dich_vu_massage_body = DichVu(
        ten_dich_vu="Massage body thư giãn",
        gia_dich_vu=300000,
        thoi_gian_dich_vu=60
    )

    dich_vu_cham_soc_da = DichVu(
        ten_dich_vu="Chăm sóc da chuyên sâu",
        gia_dich_vu=400000,
        thoi_gian_dich_vu=75
    )

    dich_vu_goi_dau = DichVu(
        ten_dich_vu="Gội đầu dưỡng sinh",
        gia_dich_vu=200000,
        thoi_gian_dich_vu=45
    )

    db.session.add_all([
        dich_vu_massage_body,
        dich_vu_cham_soc_da,
        dich_vu_goi_dau
    ])
    db.session.commit()

    # ================= KỸ THUẬT VIÊN =================
    ky_thuat_vien_massage_1 = KyThuatVien(
        ma_ktv=user_ktv_massage_tran_gia_huy.id,
        so_luong_khach=4,
        dich_vu_chuyen_mon=dich_vu_massage_body.id
    )

    ky_thuat_vien_massage_2 = KyThuatVien(
        ma_ktv=user_ktv_massage_nguyen_quoc_huy.id,
        so_luong_khach=4,
        dich_vu_chuyen_mon=dich_vu_massage_body.id
    )

    ky_thuat_vien_cham_soc_da_1 = KyThuatVien(
        ma_ktv=user_ktv_cham_soc_da_le_quang_an.id,
        so_luong_khach=2,
        dich_vu_chuyen_mon=dich_vu_cham_soc_da.id
    )

    ky_thuat_vien_cham_soc_da_2 = KyThuatVien(
        ma_ktv=user_ktv_cham_soc_da_nguyen_minh_anh.id,
        so_luong_khach=2,
        dich_vu_chuyen_mon=dich_vu_cham_soc_da.id
    )

    ky_thuat_vien_goi_dau_1 = KyThuatVien(
        ma_ktv=user_ktv_goi_dau_tran_cuc.id,
        so_luong_khach=2,
        dich_vu_chuyen_mon=dich_vu_goi_dau.id
    )

    db.session.add_all([
        ky_thuat_vien_massage_1,
        ky_thuat_vien_cham_soc_da_1,
        ky_thuat_vien_cham_soc_da_2,
        ky_thuat_vien_goi_dau_1,
        ky_thuat_vien_massage_2,
    ])
    db.session.commit()

    # ================= THỜI GIAN BIỂU KTV =================
    thoi_gian_bieu_ktv_massage_1 = ThoiGianBieuKTV(
        ma_ky_thuat_vien=ky_thuat_vien_massage_1.ma_ktv,
        t2=CaLamEnum.A,
        t3=CaLamEnum.B,
        t4=CaLamEnum.A
    )

    thoi_gian_bieu_ktv_massage_2 = ThoiGianBieuKTV(
        ma_ky_thuat_vien=ky_thuat_vien_massage_2.ma_ktv,
        t2=CaLamEnum.C,
        t3=CaLamEnum.S,
        t4=CaLamEnum.A
    )

    thoi_gian_bieu_ktv_cham_soc_da_1 = ThoiGianBieuKTV(
        ma_ky_thuat_vien=ky_thuat_vien_cham_soc_da_2.ma_ktv,
        t5=CaLamEnum.S,
        t6=CaLamEnum.C
    )

    thoi_gian_bieu_ktv_cham_soc_da_2 = ThoiGianBieuKTV(
        ma_ky_thuat_vien=ky_thuat_vien_cham_soc_da_1.ma_ktv,
        t5=CaLamEnum.B,
        t6=CaLamEnum.C
    )

    thoi_gian_bieu_ktv_goi_dau_1 = ThoiGianBieuKTV(
        ma_ky_thuat_vien=ky_thuat_vien_goi_dau_1.ma_ktv,
        t5=CaLamEnum.B,
        t6=CaLamEnum.C
    )

    db.session.add_all([
        thoi_gian_bieu_ktv_massage_1,
        thoi_gian_bieu_ktv_cham_soc_da_1,
        thoi_gian_bieu_ktv_cham_soc_da_2,
        thoi_gian_bieu_ktv_massage_2,
        thoi_gian_bieu_ktv_goi_dau_1,
    ])
    db.session.commit()

    # ================= ĐẶT LỊCH =================
    don_dat_lich_nguyen_van_a = DatLich(
        ma_khach_hang=khach_hang_nguyen_van_a.id,
        ma_le_tan=le_tan_le_thi_c.id,
        trang_thai_dat_lich=TrangThaiDatLich.DA_XAC_NHAN,
        gio_hen = datetime.now(),
        ghi_chu = "Tôi không thiếu tiền cho tôi dịch vụ tốt nhất"
    )

    don_dat_lich_nguyen_van_hoang = DatLich(
        ma_khach_hang=khach_hang_nguyen_van_hoang.id,
        ma_le_tan=le_tan_le_thi_c.id,
        trang_thai_dat_lich=TrangThaiDatLich.DA_XAC_NHAN,
        gio_hen=datetime.now() + timedelta(days=3),
        ghi_chu="Tôi thiếu tiền cho tôi dịch vụ nào cũng đc"

    )

    don_dat_lich_nguyen_van_tien = DatLich(
        ma_khach_hang=khach_hang_nguyen_van_tien.id,
        ma_le_tan=le_tan_le_thi_c.id,
        trang_thai_dat_lich=TrangThaiDatLich.CHO_XAC_NHAN,
        gio_hen=datetime.now() + timedelta(days=1),
        ghi_chu="Tôi không có ghi chú"

    )

    don_dat_lich_tran_thi_b = DatLich(
        ma_khach_hang=khach_hang_tran_thi_b.id,
        ma_le_tan=le_tan_le_thi_c.id,
        trang_thai_dat_lich=TrangThaiDatLich.DA_HUY,
        gio_hen=datetime.now() + timedelta(days=2),
        ghi_chu="no"
    )

    db.session.add_all([
        don_dat_lich_nguyen_van_a,
        don_dat_lich_nguyen_van_hoang,
        don_dat_lich_nguyen_van_tien,
        don_dat_lich_tran_thi_b
    ])
    db.session.commit()

    # ================= ĐẶT LỊCH CHI TIẾT (NHIỀU DỊCH VỤ) =================

    chi_tiet_dat_lich_massage_nguyen_van_a = DatLichDetail(
        ma_dat_lich=don_dat_lich_nguyen_van_a.id,
        ma_dich_vu=dich_vu_massage_body.id,
        ma_ky_thuat_vien=ky_thuat_vien_massage_2.ma_ktv
    )

    chi_tiet_dat_lich_goi_dau_nguyen_van_a = DatLichDetail(
        ma_dat_lich=don_dat_lich_nguyen_van_a.id,
        ma_dich_vu=dich_vu_goi_dau.id,
        ma_ky_thuat_vien=ky_thuat_vien_goi_dau_1.ma_ktv
    )

    chi_tiet_dat_lich_massage_nguyen_van_hoang = DatLichDetail(
        ma_dat_lich=don_dat_lich_nguyen_van_hoang.id,
        ma_dich_vu=dich_vu_massage_body.id,
        ma_ky_thuat_vien=ky_thuat_vien_massage_2.ma_ktv
    )

    chi_tiet_dat_lich_cham_soc_da_nguyen_van_hoang = DatLichDetail(
        ma_dat_lich=don_dat_lich_nguyen_van_hoang.id,
        ma_dich_vu=dich_vu_cham_soc_da.id,
        ma_ky_thuat_vien=ky_thuat_vien_cham_soc_da_2.ma_ktv
    )
    chi_tiet_dat_lich_doi_dau_nguyen_van_hoang = DatLichDetail(
        ma_dat_lich=don_dat_lich_nguyen_van_hoang.id,
        ma_dich_vu=dich_vu_goi_dau.id,
        ma_ky_thuat_vien=ky_thuat_vien_goi_dau_1.ma_ktv
    )

    chi_tiet_dat_lich_massage_nguyen_van_tien = DatLichDetail(
        ma_dat_lich=don_dat_lich_nguyen_van_tien.id,
        ma_dich_vu=dich_vu_massage_body.id,
        ma_ky_thuat_vien=None
    )

    chi_tiet_dat_lich_goi_dau_nguyen_van_tien = DatLichDetail(
        ma_dat_lich=don_dat_lich_nguyen_van_tien.id,
        ma_dich_vu=dich_vu_goi_dau.id,
        ma_ky_thuat_vien=None
    )

    chi_tiet_dat_lich_massage_tran_thi_b = DatLichDetail(
        ma_dat_lich=don_dat_lich_tran_thi_b.id,
        ma_dich_vu=dich_vu_massage_body.id,
        ma_ky_thuat_vien=ky_thuat_vien_massage_1.ma_ktv
    )

    db.session.add_all([
        chi_tiet_dat_lich_doi_dau_nguyen_van_hoang,
        chi_tiet_dat_lich_massage_nguyen_van_hoang,
        chi_tiet_dat_lich_cham_soc_da_nguyen_van_hoang,
        chi_tiet_dat_lich_massage_tran_thi_b,
        chi_tiet_dat_lich_goi_dau_nguyen_van_tien,
        chi_tiet_dat_lich_massage_nguyen_van_tien,
        chi_tiet_dat_lich_goi_dau_nguyen_van_a,
        chi_tiet_dat_lich_massage_nguyen_van_a
    ])
    db.session.commit()

    # ================= PHIẾU DỊCH VỤ =================
    phieu_dich_vu_nguyen_van_a = PhieuDichVu(
        ma_dat_lich=don_dat_lich_nguyen_van_a.id
    )

    phieu_dich_vu_nguyen_van_hoang = PhieuDichVu(
        ma_dat_lich=don_dat_lich_nguyen_van_hoang.id
    )

    phieu_dich_vu_nguyen_van_tien = PhieuDichVu(
        ma_dat_lich=don_dat_lich_nguyen_van_tien.id
    )

    phieu_dich_vu_tran_thi_b = PhieuDichVu(
        ma_dat_lich=don_dat_lich_tran_thi_b.id
    )

    db.session.add_all([
        phieu_dich_vu_nguyen_van_a,
        phieu_dich_vu_nguyen_van_hoang,
        phieu_dich_vu_nguyen_van_tien,
        phieu_dich_vu_tran_thi_b
    ])
    db.session.commit()


    phieu_dich_vu_ct_cham_soc_da_nguyen_van_a = PhieuDichVuDetail(
        ma_phieu_dich_vu=phieu_dich_vu_nguyen_van_a.id,
        ma_dich_vu=dich_vu_massage_body.id,
        ghi_chu_ktv="Khách thư giãn tốt"
    )

    phieu_dich_vu_ct_goi_dau_nguyen_van_a = PhieuDichVuDetail(
        ma_phieu_dich_vu=phieu_dich_vu_nguyen_van_a.id,
        ma_dich_vu=dich_vu_goi_dau.id,
        ghi_chu_ktv="Khách hài lòng"
    )

    phieu_dich_vu_ct_massage_nguyen_van_hoang = PhieuDichVuDetail(
        ma_phieu_dich_vu=phieu_dich_vu_nguyen_van_hoang.id,
        ma_dich_vu=dich_vu_massage_body.id,
        ghi_chu_ktv="Khách thư giãn tốt"
    )
    phieu_dich_vu_ct_cham_soc_da_nguyen_van_hoang = PhieuDichVuDetail(
        ma_phieu_dich_vu=phieu_dich_vu_nguyen_van_hoang.id,
        ma_dich_vu=dich_vu_cham_soc_da.id,
        ghi_chu_ktv="Khách thư giãn tốt"
    )

    phieu_dich_vu_ct_goi_dau_nguyen_van_hoang = PhieuDichVuDetail(
        ma_phieu_dich_vu=phieu_dich_vu_nguyen_van_hoang.id,
        ma_dich_vu=dich_vu_goi_dau.id,
        ghi_chu_ktv="Khách hài lòng"
    )

    phieu_dich_vu_ct_cham_soc_da_nguyen_van_tien = PhieuDichVuDetail(
        ma_phieu_dich_vu=phieu_dich_vu_nguyen_van_tien.id,
        ma_dich_vu=dich_vu_cham_soc_da.id,
        ghi_chu_ktv="Khách hài lòng"
    )

    phieu_dich_vu_ct_massage_nguyen_van_tien = PhieuDichVuDetail(
        ma_phieu_dich_vu=phieu_dich_vu_nguyen_van_tien.id,
        ma_dich_vu=dich_vu_massage_body.id,
        ghi_chu_ktv="Khách thư giãn tốt"
    )

    phieu_dich_vu_ct_massage_tran_thi_b = PhieuDichVuDetail(
        ma_phieu_dich_vu=phieu_dich_vu_tran_thi_b.id,
        ma_dich_vu=dich_vu_massage_body.id,
        ghi_chu_ktv="Khách hài lòng"
    )

    db.session.add_all([
       phieu_dich_vu_ct_cham_soc_da_nguyen_van_a,
        phieu_dich_vu_ct_goi_dau_nguyen_van_a,
        phieu_dich_vu_ct_cham_soc_da_nguyen_van_hoang,
        phieu_dich_vu_ct_goi_dau_nguyen_van_hoang,
        phieu_dich_vu_ct_massage_nguyen_van_hoang,
        phieu_dich_vu_ct_massage_nguyen_van_tien,
        phieu_dich_vu_ct_cham_soc_da_nguyen_van_tien,
        phieu_dich_vu_ct_massage_tran_thi_b,
    ])
    db.session.commit()

    # ================= VAT & MÃ GIẢM GIÁ =================
    vat_hien_hanh = VAT(muc_vat=0.08)
    db.session.add(vat_hien_hanh)
    db.session.commit()

    ma_giam_gia_spa_massage = MaGiamGia(
        ten_ma_giam_gia="Giam_Gia_DV_Massage",
        muc_giam_gia=0.1,
        ngay_bat_dau=datetime.now(),
        ngay_het_han=datetime.now() + timedelta(days=30),
        ma_dich_vu=dich_vu_massage_body.id
    )

    ma_giam_gia_spa_cham_soc_da = MaGiamGia(
        ten_ma_giam_gia="Giam_Gia_DV_Cham_Soc_da",
        muc_giam_gia=0.2,
        ngay_bat_dau=datetime.now(),
        ngay_het_han=datetime.now() + timedelta(days=30),
        ma_dich_vu=dich_vu_cham_soc_da.id,
    )

    ma_giam_gia_spa_goi_dau = MaGiamGia(
        ten_ma_giam_gia="Giam_GiaDV_Goi_dau",
        muc_giam_gia=0.05,
        ngay_bat_dau=datetime.now(),
        ngay_het_han=datetime.now() + timedelta(days=30),
        ma_dich_vu=dich_vu_goi_dau.id,
    )

    db.session.add_all([
        ma_giam_gia_spa_goi_dau,
        ma_giam_gia_spa_massage,
        ma_giam_gia_spa_cham_soc_da,
    ])
    db.session.commit()

    # ================= KHÁCH HÀNG - MÃ GIẢM GIÁ =================
    ma_giam_gia_khach_hang_nguyen_van_a = KhachHangMaGiamGia(
        ma_khach_hang=khach_hang_nguyen_van_a.id,
        ma_giam_gia=ma_giam_gia_spa_massage.id,
        trang_thai=TrangThaiMaGiamGiaEnum.CHUA_SU_DUNG
    )

    ma_giam_gia_khach_hang_nguyen_van_hoang = KhachHangMaGiamGia(
        ma_khach_hang=khach_hang_nguyen_van_hoang.id,
        ma_giam_gia=ma_giam_gia_spa_goi_dau.id,
        trang_thai=TrangThaiMaGiamGiaEnum.CHUA_SU_DUNG
    )

    ma_giam_gia_khach_hang_nguyen_van_tien = KhachHangMaGiamGia(
        ma_khach_hang=khach_hang_nguyen_van_tien.id,
        ma_giam_gia=ma_giam_gia_spa_cham_soc_da.id,
        trang_thai=TrangThaiMaGiamGiaEnum.CHUA_SU_DUNG
    )

    ma_giam_gia_khach_hang_tran_thi_b = KhachHangMaGiamGia(
        ma_khach_hang=khach_hang_tran_thi_b.id,
        ma_giam_gia=ma_giam_gia_spa_goi_dau.id,
        trang_thai=TrangThaiMaGiamGiaEnum.CHUA_SU_DUNG
    )

    db.session.add_all([
        ma_giam_gia_khach_hang_nguyen_van_hoang,
        ma_giam_gia_khach_hang_nguyen_van_a,
        ma_giam_gia_khach_hang_tran_thi_b,
        ma_giam_gia_khach_hang_nguyen_van_tien
    ])
    db.session.commit()

    # ================= HÓA ĐƠN =================
    hoa_don_nguyen_van_a = HoaDon(
        ma_thu_ngan = thu_ngan_pham_van_d.id,
        ma_phieu_dich_vu=phieu_dich_vu_nguyen_van_a.id,
        ma_vat=vat_hien_hanh.id,
        tong_gia_dich_vu=500000,
        tong_thanh_toan=486000,
        thoi_gian_thanh_toan=datetime.now()
    )

    hoa_don_nguyen_van_hoang = HoaDon(
        ma_thu_ngan=thu_ngan_pham_van_d.id,
        ma_phieu_dich_vu=phieu_dich_vu_nguyen_van_hoang.id,
        ma_vat=vat_hien_hanh.id,
        tong_gia_dich_vu=500000,
        tong_thanh_toan=486000,
        thoi_gian_thanh_toan=datetime.now()
    )

    hoa_don_nguyen_van_tien = HoaDon(
        ma_thu_ngan=thu_ngan_pham_van_d.id,
        ma_phieu_dich_vu=phieu_dich_vu_nguyen_van_tien.id,
        ma_vat=vat_hien_hanh.id,
        tong_gia_dich_vu=500000,
        tong_thanh_toan=486000,
        thoi_gian_thanh_toan=datetime.now()
    )

    hoa_don_tran_thi_b = HoaDon(
        ma_thu_ngan=thu_ngan_pham_van_d.id,
        ma_phieu_dich_vu=phieu_dich_vu_tran_thi_b.id,
        ma_vat=vat_hien_hanh.id,
        tong_gia_dich_vu=500000,
        tong_thanh_toan=486000,
        thoi_gian_thanh_toan=datetime.now()
    )

    db.session.add_all([
        hoa_don_nguyen_van_a,
        hoa_don_nguyen_van_hoang,
        hoa_don_nguyen_van_tien,
        hoa_don_tran_thi_b,

    ])
    db.session.commit()

    print("✅ Seed data rõ ràng – đúng mối quan hệ – đúng models")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_data_ro_rang()
