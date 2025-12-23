from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_login import current_user, logout_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea

from spa_app.models import DichVu, User, KyThuatVien, VAT, MaGiamGia, KhachHangMaGiamGia, UserRole
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
        # KHÔNG có 'hoa_don'
    ]
    column_labels = {
        'muc_vat': "Mức VAT",
        'ngay_tao':'Ngày Tạo'
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
        'trang_thai':"Trạng thái mã giảm giá"
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

admin = Admin(app=app, name="SPA_APP", theme=Bootstrap4Theme(), index_view=MyAdminIndexView())


admin.add_view(MyUserView(User, db.session))
admin.add_view(MyKyThuatVienView(KyThuatVien,db.session))
admin.add_view(MyDichVuView(DichVu, db.session))
admin.add_view(MyVatView(VAT,db.session))
admin.add_view(MyMaGiamGiaView(MaGiamGia,db.session))
admin.add_view(MyKhMaGiamGiaView(KhachHangMaGiamGia,db.session))
admin.add_view(MyAdminLogoutView("Đăng xuất"))