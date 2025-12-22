function displayInvoice(serviceSheetId){
    window.location.href = "/invoices/" + serviceSheetId + window.location.search;
}

function closeInvoice(){
    window.location.href = "/invoices/0" + window.location.search;
}

function findDiscount(serviceSheetId, customerId){
    let discount = document.getElementById("find_discount").value;

    fetch(`/invoices/${serviceSheetId}/add_discount`,{
        method: "put",
        body: JSON.stringify({
            "ma_giam_gia": discount,
            "ma_khach_hang": customerId
        }),
        headers: {
            "content-type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        if(data.status===400) {
            let alert = document.getElementById("alertSelect");
            alert.innerHTML="<strong>Thông báo!</strong> "+data.err_msg;
            alert.style.display="block";
            setTimeout(() => {alert.style.display = "none";}, 3000);
            document.getElementById("find_discount").value = null;
        }
        else {
            location.reload();
        }
    });
}

function removeDiscount(serviceSheetId, serviceId){
    if(confirm("Bạn có chắc chắn muốn gỡ mã giảm giá?")===true){
        fetch(`/invoices/${serviceSheetId}/remove_discount`,{
            method: "put",
            body: JSON.stringify({
                "ma_dich_vu": serviceId,
            }),
            headers: {
                "content-type": "application/json"
            }
        }).then(res => res.json()).then(data => {
            if(data.status===400) {
                let alert = document.getElementById("alertSelect");
                alert.innerHTML="<strong>Thông báo!</strong> "+data.err_msg;
                alert.style.display="block";
                setTimeout(() => {alert.style.display = "none";}, 3000);
                document.getElementById("find_discount").value = null;
            }
            else {
                location.reload();
            }
        });
    }
}

function handlePaidInput(input) {
    let rawValue = input.value.replace(/\D/g, "");

    const paidRealInput = document.getElementById("paidReal");
    const total = Math.round(Number(document.getElementById("totalReal").value));
    const resultDisplay = document.getElementById("resultDisplay");
    const btnPay = document.getElementById("btnPay");

    if (rawValue === "") {
        input.value = "";
        paidRealInput.value = "";
        resultDisplay.value = "";
        btnPay.disabled = true;
        return;
    }

    let paid = Math.round(parseInt(rawValue, 10));
    paidRealInput.value = paid;

    input.value = formatVND(paid);

    let diff = parseInt(paid - total);

    if (diff >= 0) {
        resultDisplay.value = "Tiền thừa: " + formatVND(diff) + " VND";
        resultDisplay.classList.remove("text-danger");
        resultDisplay.classList.add("text-success");
        btnPay.disabled = false;
    } else {
        resultDisplay.value = "Còn thiếu: " + formatVND(Math.abs(diff)) + " VND";
        resultDisplay.classList.remove("text-success");
        resultDisplay.classList.add("text-danger");
        btnPay.disabled = true;
    }
}

function formatVND(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function successPaid(serviceSheetId){
    let paymentMethod = null;
    let total = null;
    let paid = null;

    if (document.querySelector('a.nav-link.active[href="#cash"]')){
        paymentMethod = 'TIEN_MAT';
        total = document.getElementById('totalReal').value;
        paid = document.getElementById('paidReal').value;
    }
    else {
        paymentMethod = 'CHUYEN_KHOAN';
        total = document.getElementById('totalReal').value;
        paid = total;
    }

    if (!paid) {
        let alert = document.getElementById("alertSelect");
        alert.innerHTML="<strong>Thông báo!</strong> Chưa nhập số tiền khách đưa";
        alert.style.display="block";
        setTimeout(() => {alert.style.display = "none";}, 3000);
        return;
    } else if (paid - total < 0){
        let alert = document.getElementById("alertSelect");
        alert.innerHTML="<strong>Thông báo!</strong> Số tiền nhận chưa hợp lệ";
        alert.style.display="block";
        setTimeout(() => {alert.style.display = "none";}, 3000);
        return;
    }

    let temporary = document.getElementById('temporary').innerHTML;
    temporary = Number(temporary.replace(/,/g, ''));

    let total_discount = document.getElementById('total_discount').innerHTML;
    total_discount = Number(total_discount.replace(/,/g, ''));

    fetch(`/invoices/${serviceSheetId}/payment/success`,{
        method: "post",
        body: JSON.stringify({
            "phuong_thuc": paymentMethod,
            "tong_dich_vu": temporary,
            "tong_giam_gia": total_discount,
            "tong_thanh_toan": total,
            "so_tien_nhan": paid,
        }),
        headers: {
            "content-type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        if(data.status===500) {
            let alert = document.getElementById("alertSelect");
            alert.innerHTML="<strong>Thông báo!</strong> "+data.err_msg;
            alert.style.display="block";
            setTimeout(() => {alert.style.display = "none";}, 3000);
        }
        else {
            window.print();
            window.location.href = "/invoices/" + serviceSheetId +'?page=1';
        }
    });
}