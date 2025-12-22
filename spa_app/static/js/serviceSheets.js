function displaySheetDetail(appointmentId){
    window.location.href = "/serviceSheets/" + appointmentId + window.location.search;
}

function closeSheetDetail(){
    window.location.href = "/serviceSheets/0" + window.location.search;
}

function startUpdateSD(appointmentId){
    window.location.href = "/serviceSheets/update/" + appointmentId + window.location.search;
}

function cancelUpdateSD(appointmentId){
    window.location.href = "/serviceSheets/" + appointmentId + window.location.search;
}

function changeForUpdateSD(){
    document.getElementById("btnUpdate").style.display = "none";
    document.getElementById("btnForUpdate").style.display = "flex";
    document.getElementById("noteArea").style.background = "white";
    document.getElementById("serviceNote").style.background = "white";
    document.getElementById("serviceNote").readOnly = false;
    document.getElementById("replyArea").style.background = "white";
    document.getElementById("customerReply").style.background = "white";
    document.getElementById("customerReply").readOnly = false;
}

function successUpdateSD(serviceId, appointmentId) {
    let updateContent = {
        ma_dich_vu: serviceId,
        ghi_chu: document.getElementById("serviceNote").value,
        phan_hoi: document.getElementById("customerReply").value
    };

    fetch(`/serviceSheets/update/${appointmentId}/success`,{
        method: "post",
        body: JSON.stringify(updateContent),
        headers: {
            "content-type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        if (data.status==200) {
            window.location.href = "/serviceSheets/" + appointmentId +"?page=1";
        }
        else{
            alert(data.err_msg)
        }
    });
}