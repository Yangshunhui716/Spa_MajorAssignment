document.addEventListener('DOMContentLoaded', () => {
  const serviceList = document.getElementById('service-list');
  const durationEl = document.getElementById('duration');
  const addBtn = document.getElementById('add-service-btn');
  const overlay = document.getElementById('booking-overlay');
  const form = document.querySelector("form"); // lấy form thực sự
  const bookingBtn = document.getElementById('booking-btn');
  const icon = document.getElementById("schedule-icon");

  // Mở overlay khi click icon 📅
  if(icon){
    icon.addEventListener("click", () => {
      overlay.style.display = "block";
    });
  }

  // Đóng overlay khi click ngoài form
  overlay.addEventListener("click", (e) => {
    if (!form.contains(e.target)) {
      overlay.style.display = "none";
    }
  });

  // Tạo item dịch vụ
  function createServiceItem() {
    const wrapper = document.createElement('div');
    wrapper.className = 'd-flex align-items-center mb-2 service-item';

    const select = document.createElement('select');
    select.className = 'form-select service-select';
    select.innerHTML = `
      <option value="20">Massage Mặt - 20 phút</option>
      <option value="30">Điều trị mụn - 30 phút</option>
      <option value="25">Triệt lông - 25 phút</option>
    `;

    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.className = 'remove-btn';
    removeBtn.innerHTML = '×';

    wrapper.appendChild(select);
    wrapper.appendChild(removeBtn);
    return wrapper;
  }

  // Cập nhật tổng thời gian
  function updateDuration() {
    const selects = serviceList.querySelectorAll('.service-select');
    let total = 0;
    selects.forEach(s => total += parseInt(s.value, 10));
    durationEl.textContent = total + ' phút';
  }

  // Cập nhật trạng thái nút xoá
  function updateRemoveButtons() {
    const items = serviceList.querySelectorAll('.service-item');
    const buttons = serviceList.querySelectorAll('.remove-btn');
    const canRemove = items.length > 1;
    buttons.forEach(btn => {
      btn.disabled = !canRemove;
      btn.classList.toggle('active', canRemove);
      btn.style.cursor = canRemove ? 'pointer' : 'not-allowed';
    });
  }

  // Thêm dịch vụ
  addBtn.addEventListener('click', () => {
    const item = createServiceItem();
    serviceList.appendChild(item);
    updateDuration();
    updateRemoveButtons();
  });

  // Xoá dịch vụ
  serviceList.addEventListener('click', (e) => {
    if (e.target.classList.contains('remove-btn')) {
      e.preventDefault();
      e.stopPropagation();
      const items = serviceList.querySelectorAll('.service-item');
      if (items.length > 1) {
        const item = e.target.closest('.service-item');
        if (item) {
          item.remove();
          updateDuration();
          updateRemoveButtons();
        }
      }
    }
  });

  // Thay đổi dịch vụ → cập nhật thời gian
  serviceList.addEventListener('change', (e) => {
    if (e.target.classList.contains('service-select')) {
      updateDuration();
    }
  });

  // Kiểm tra form khi bấm Đặt lịch
  bookingBtn.addEventListener('click', (e) => {
    const name = document.getElementById('name').value.trim();
    const date = document.getElementById('date').value.trim();
    const time = document.getElementById('time').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const email = document.getElementById('email').value.trim();

    // Kiểm tra bắt buộc
    if (!name || !date || !time || !phone || !email) {
      e.preventDefault(); // chặn submit nếu thiếu dữ liệu
      alert("⚠️ Vui lòng nhập đầy đủ thông tin bắt buộc!");
      return;
    }

    // Kiểm tra email hợp lệ
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      e.preventDefault();
      alert("⚠️ Email không hợp lệ!");
      return;
    }

    // Kiểm tra số điện thoại (chỉ số, tối thiểu 9 ký tự)
    const phoneRegex = /^[0-9]{9,}$/;
    if (!phoneRegex.test(phone)) {
      e.preventDefault();
      alert("⚠️ Số điện thoại không hợp lệ!");
      return;
    }

    // Nếu hợp lệ → KHÔNG chặn submit, để form gửi về Flask
    // Không reset input ở đây
  });

  // Khởi tạo
  updateDuration();
  updateRemoveButtons();
});

document.addEventListener('DOMContentLoaded', () => {
  const openBtn = document.getElementById('open-booking');
  const overlay = document.getElementById('booking-overlay');
  const form = document.querySelector(".booking-form");

  // Mở overlay khi bấm nút
  openBtn.addEventListener('click', (e) => {
    e.preventDefault(); // chặn cuộn trang
    overlay.style.display = "block";
  });

  // Đóng overlay khi click ngoài form
  overlay.addEventListener('click', (e) => {
    if (!form.contains(e.target)) {
      overlay.style.display = "none";
    }
  });
});
