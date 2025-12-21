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
    const total = Number(document.getElementById("totalReal").value);
    const resultDisplay = document.getElementById("resultDisplay");
    const btnPay = document.getElementById("btnPay");

    if (rawValue === "") {
        input.value = "";
        paidRealInput.value = "";
        resultDisplay.value = "";
        btnPay.disabled = true;
        return;
    }

    let paid = parseInt(rawValue, 10);
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