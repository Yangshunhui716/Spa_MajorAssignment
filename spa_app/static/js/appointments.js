function displayAppointmentDetail(appointmentId){
    if(!window.location.href.includes("update/"+appointmentId)){
        window.location.href = "/appointments/" + appointmentId + window.location.search;
    }
}

function closeAppointmentDetail(){
    window.location.href = "/appointments/0" + window.location.search;
}

function startUpdateAD(appointmentId, serviceTherapistPairs){
    window.location.href = "/appointments/update/" + appointmentId + window.location.search;
}

function changeForUpdateAD(){
    document.getElementById("btnChangeState").style.display = "none";
    document.getElementById("btnForUpdate").style.display = "flex";
    let remove = document.getElementsByName("remove");
    let selectSrv = document.getElementsByName("selectService");
    let selectThrp = document.getElementsByName("selectTherapist");
    remove.forEach(rm => rm.style.visibility = "visible");
    selectSrv.forEach(sl => sl.disabled = false);
    selectThrp.forEach(sl => sl.disabled = false);
    document.getElementById("addService").style.visibility = "visible";
}

function addService(){
    let newDiv = document.createElement("div");
    newDiv.style = "width: 95%";
    newDiv.className = "row g-2 pt-1 pb-1 align-items-center";
    newDiv.innerHTML = `
      <select name="selectService" class="form-select col me-3">
        <option>Massage</option>
      </select>
      <select name="selectTherapist" class="form-select col ms-3 me-3">
        <option>Anna</option>
      </select>
      <button class="btn btn-dark rounded-circle d-flex align-items-center justify-content-center"
              style="width: 25px; height: 25px"
              id="remove" onclick="removeService(this)">&times;</button>
    `;
    document.getElementById("addArea").appendChild(newDiv);
}

function removeService(object){
    let div = object.parentNode;
    div.style.display="none";
}

function cancelUpdateAD(appointmentId){
    window.location.href = "/appointments/" + appointmentId;
}