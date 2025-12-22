function displayAppointmentDetail(appointmentId){
    if(!window.location.href.includes("update/"+appointmentId)){
        window.location.href = "/appointments/" + appointmentId + window.location.search;
    }
}

function closeAppointmentDetail(){
    window.location.href = "/appointments/0" + window.location.search;
}

function successAppointment(appointmentId) {
    let selectedTherapists = [];

    for (let choice of document.querySelectorAll("select[name='therapist']")) {
        if (!choice.value) {
            let alert = document.getElementById("alertSelect");
            alert.innerHTML="<strong>Thông báo!</strong> Chưa chọn kỹ thuật viên";
            alert.style.display="block";
            setTimeout(() => {alert.style.display = "none";}, 3000);
            return;
        } else {
            selectedTherapists.push({"ma_ktv":choice.value})
        }
    }

    fetch(`/appointments/${appointmentId}/success`,{
        method: "post",
        body: JSON.stringify({selectedTherapists}),
        headers: {
            "content-type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        if (data.status==200) {
            location.reload();
        }
        else{
            let alert = document.getElementById("alertSelect");
            alert.innerHTML="<strong>Thông báo!</strong> " + data.err_msg;
            alert.style.display="block";
            setTimeout(() => {alert.style.display = "none";}, 3000);
        }
    });
}