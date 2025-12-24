document.addEventListener('DOMContentLoaded', () => {
  const serviceList = document.getElementById('service-list');
  const durationEl = document.getElementById('duration');
  const addBtn = document.getElementById('add-service-btn');
  const hidden = document.getElementById('hidden-services');
  const bookingBtn = document.getElementById('booking-btn');
  const bookingForm = document.querySelector('.booking-form');

  // ================= TẠO 1 DÒNG DỊCH VỤ =================

  console.log("list_services =", list_services);
  function createServiceItem() {
  const wrapper = document.createElement('div');
  wrapper.className = 'd-flex align-items-center mb-2 service-item';

  const select = document.createElement('select');
  select.className = 'form-select service-select';

  select.innerHTML = '<option value="">-- Chọn dịch vụ --</option>';

  list_services.forEach(dv => {
    const option = document.createElement('option');
    option.value = dv.id;
    option.textContent = `${dv.ten} - ${dv.thoi_gian} phút`;
    option.dataset.time = dv.thoi_gian;
    select.appendChild(option);
  });

  const removeBtn = document.createElement('button');
  removeBtn.type = 'button';
  removeBtn.className = 'remove-btn';
  removeBtn.innerHTML = '×';

  wrapper.appendChild(select);
  wrapper.appendChild(removeBtn);
  return wrapper;
}


  // ================= TÍNH TỔNG THỜI GIAN =================
  function updateDuration() {
    let total = 0;
    const selects = serviceList.querySelectorAll('.service-select');

    selects.forEach(select => {
      const opt = select.selectedOptions[0];
      if (!opt) return;
      total += Number(opt.dataset.time || 0);
    });

    durationEl.textContent = total + ' phút';
  }

  // ================= SYNC HIDDEN =================
  function syncHiddenServices() {
    hidden.innerHTML = '';
    const selects = serviceList.querySelectorAll('.service-select');
    const used = new Set();

    selects.forEach(select => {
      if (!select.value || used.has(select.value)) return;
      used.add(select.value);

      const input = document.createElement('input');
      input.type = 'hidden';
      input.name = 'services[]';
      input.value = select.value;
      hidden.appendChild(input);
    });
  }

  // ================= THÊM DỊCH VỤ =================
  addBtn.addEventListener('click', () => {
    serviceList.appendChild(createServiceItem());
  });

  // ================= XOÁ DỊCH VỤ =================
  serviceList.addEventListener('click', e => {
    if (e.target.classList.contains('remove-btn')) {
      const items = serviceList.querySelectorAll('.service-item');
      if (items.length > 1) {
        e.target.closest('.service-item').remove();
        updateDuration();
        syncHiddenServices();
      }
    }
  });

  // ================= ĐỔI DỊCH VỤ =================
  serviceList.addEventListener('change', e => {
    if (e.target.classList.contains('service-select')) {
      updateDuration();
      syncHiddenServices();
    }
  });

  // ================= SUBMIT JSON =================
  bookingBtn.addEventListener('click', e => {
    e.preventDefault();

    const services = [];
     const used = new Set();
    const selects = serviceList.querySelectorAll('.service-select');



    const name  = document.getElementById('name').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const email = document.getElementById('email').value.trim();
    const date  = document.getElementById('date').value;
    const time  = document.getElementById('time').value;
    const note  = document.getElementById('note').value;

      console.log({ name, phone, date, time });



     if (!name || !phone || !date || !time) {
        alert('❌ Vui lòng nhập đầy đủ Họ tên, SĐT, Ngày và Giờ');
        return;
      }

     if (!/^[0-9]{9,11}$/.test(phone)) {
        alert('❌ Số điện thoại không hợp lệ');
        return;
      }



     document.querySelectorAll('.service-select').forEach(select => {
      if (!select.value || used.has(select.value)) return;

         used.add(select.value);

        const opt = select.selectedOptions[0];
        services.push({
            id: select.value,
            time: Number(opt?.dataset?.time || 0)
          });
        });

    console.log (services)

    if (used.length === 0) {
      alert('❌ Vui lòng chọn ít nhất 1 dịch vụ');
      return;
    }

    data ={
        "name" : name,
        "phone": phone,
        "date": date,
        "time":time,
        "email":email,
        "note":note,
        "services": services

      }

     fetch('/booking', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
      alert(res.message || 'Đã tiếp nhận đơn đặt lịch! Bạn đợi bộ phận lễ tân liên hệ xác nhận đặt lịch thành công sau nhá!');
    })
    .catch(() => alert('Có lỗi xảy ra'));


  });

  updateDuration();
});
