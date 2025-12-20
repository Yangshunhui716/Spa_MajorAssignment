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