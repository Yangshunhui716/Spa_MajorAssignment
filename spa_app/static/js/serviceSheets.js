function displaySheetDetail(serviceSheetId){
    window.location.href = "/serviceSheets/" + serviceSheetId + window.location.search;
}

function closeSheetDetail(){
    window.location.href = "/serviceSheets/0" + window.location.search;
}

function startUpdateSD(serviceSheetId){
    window.location.href = "/serviceSheets/update/" + serviceSheetId + window.location.search;
}

function cancelUpdateSD(serviceSheetId){
    window.location.href = "/serviceSheets/" + serviceSheetId;
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

