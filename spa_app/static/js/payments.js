function displayInvoice(serviceSheetId){
    window.location.href = "/payments/" + serviceSheetId + window.location.search;
}

function closeInvoice(){
    window.location.href = "/payments/0" + window.location.search;
}

