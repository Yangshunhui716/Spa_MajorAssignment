import hashlib
import json
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_login import current_user, logout_user
from sqlalchemy import extract, func
from wtforms import TextAreaField
from wtforms.widgets import TextArea

from spa_app.models import DichVu, User, KyThuatVien, VAT, MaGiamGia, KhachHangMaGiamGia, UserRole, ThoiGianBieuKTV, \
    ThoiGianKTVBan, HoaDon, PhieuDichVuDetail, PhieuDichVu
from spa_app import app, db, models


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class AuthenTicatedView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.role_user == UserRole.QUAN_LY


class AdminModeView(BaseView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.role_user == UserRole.QUAN_TRI_VIEN


class MyUserView(AuthenTicatedView):
    column_searchable_list = ['sdt_user']
    column_filters = ['sdt_user']
    column_labels = {
        'ho_ten_user': "Họ và Tên",
        'sdt_user': "Số điện thoại",
        'email_user': "Email",
        'tai_khoan_user': "Tên Tài Khoản",
        'password_user': "Mật Khẩu",
    }

    def on_model_change(self, form, model, is_created):
        if is_created and model.password_user:
            model.password_user = hashlib.md5(model.password_user.encode('utf-8')).hexdigest()


class MyKyThuatVienView(AuthenTicatedView):
    # column_searchable_list = ['sdt_user']
    # column_filters = ['sdt_user']
    column_labels = {
        'user': "Tên User",
        'dich_vu': "Dịch vụ chuyên môn",
        'so_luong_khach': "Số lượng khách",
    }


class MyDichVuView(AuthenTicatedView):
    # column_searchable_list = ['sdt_user']
    # column_filters = ['sdt_user']
    column_labels = {
        'ten_dich_vu': "Tên dịch vụ",
        'mo_ta': "Mô tả",
        'gia_dich_vu': "Giá",
        'thoi_gian_dich_vu': "Thời gian",
        'thoi_gian_nghi_ngoi': "Thời gian KTV nghỉ",
        'gioi_han_khach': "Giới hạn khách",
        'ngay_tao': "Ngày tạo",

    }


class MyVatView(AuthenTicatedView):
    form_columns = [
        'muc_vat'
    ]
    column_labels = {
        'muc_vat': "Mức VAT",
        'ngay_tao': 'Ngày Tạo'
    }


class MyMaGiamGiaView(AuthenTicatedView):
    column_labels = {
        'ten_ma_giam_gia': "Tên mã giảm giá",
        'mo_ta': "Mô tả",
        'muc_giam_gia': "Mức Giảm",
        'ngay_bat_dau': "Thời gian bắt đầu",
        'ngay_het_han': "Thời gian hết hạn",
        'ngay_tao': "Ngày tạo",
        'dich_vu': "Dịch vụ áp dụng",
    }


class MyKhMaGiamGiaView(AuthenTicatedView):
    column_labels = {
        'trang_thai': "Trạng thái mã giảm giá"
    }


class MyTGBKtvView(AuthenTicatedView):
    column_labels = {
        'ky_thuat_vien': "Mã kỹ thuật viên"
    }

class MyTGBKtvBanView(AuthenTicatedView):
    column_labels = {
        'thoi_gian_bat_dau': "Thời gian bắt đầu",
        'thoi_gian_ket_thuc': "Thời gian kết thúc"
    }


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self) -> str:
        return self.render("admin/index.html")


class MyAdminLogoutView(BaseView):
    @expose("/")
    def index(self) -> str:
        logout_user()
        return self.render("admin/index.html")


class ThongKeView(AdminModeView):

    @expose('/')
    def index(self):
        doanh_thu_thang = (
            db.session.query(
                extract('month', PhieuDichVu.ngay_tao).label('thang'),
                func.sum(DichVu.gia_dich_vu).label('doanh_thu')
            )
            .select_from(PhieuDichVuDetail)  # 🔥 CHỐT BẢNG GỐC
            .join(
                PhieuDichVu,
                PhieuDichVu.id == PhieuDichVuDetail.ma_phieu_dich_vu
            )
            .join(
                DichVu,
                DichVu.id == PhieuDichVuDetail.ma_dich_vu
            )
            .group_by('thang')
            .order_by('thang')
            .all()
        )

        tan_suat_dich_vu = (
            db.session.query(
                extract('month', PhieuDichVu.ngay_tao).label('thang'),
                DichVu.ten_dich_vu,
                func.count(PhieuDichVuDetail.ma_dich_vu).label('so_lan')
            )
            .select_from(PhieuDichVuDetail)
            .join(
                PhieuDichVu,
                PhieuDichVu.id == PhieuDichVuDetail.ma_phieu_dich_vu
            )
            .join(
                DichVu,
                DichVu.id == PhieuDichVuDetail.ma_dich_vu
            )
            .group_by('thang', DichVu.ten_dich_vu)
            .order_by('thang')
            .all()
        )

        doanh_thu_chart = {
            "labels": [f"Tháng {t}" for t, _ in doanh_thu_thang],
            "data": [dt for _, dt in doanh_thu_thang]
        }

        # Tần suất dịch vụ (biểu đồ tròn theo từng tháng)
        tan_suat_chart = {}
        for thang, ten_dv, so_lan in tan_suat_dich_vu:
            tan_suat_chart.setdefault(f"Tháng {thang}", {})
            tan_suat_chart[f"Tháng {thang}"][ten_dv] = so_lan

        return self.render(
            'admin/report.html',
            doanh_thu_thang=doanh_thu_thang,
            tan_suat_dich_vu=tan_suat_dich_vu,
            doanh_thu_chart=doanh_thu_chart,
            tan_suat_chart=tan_suat_chart
        )


admin = Admin(app=app, name="SPA_APP", theme=Bootstrap4Theme(), index_view=MyAdminIndexView())

admin.add_view(MyUserView(User, db.session))
admin.add_view(MyKyThuatVienView(KyThuatVien, db.session))
admin.add_view(MyDichVuView(DichVu, db.session))
admin.add_view(MyVatView(VAT, db.session))
admin.add_view(MyMaGiamGiaView(MaGiamGia, db.session))
admin.add_view(MyKhMaGiamGiaView(KhachHangMaGiamGia, db.session))
admin.add_view(MyTGBKtvView(ThoiGianKTVBan, db.session))
admin.add_view(MyTGBKtvBanView(ThoiGianBieuKTV, db.session))

admin.add_view(ThongKeView(name="Thống kê - Báo cáo", endpoint="thongke"))
admin.add_view(MyAdminLogoutView("Đăng xuất"))

