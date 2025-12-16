function search(){
    let kw = document.getElementById("search").value;
    if (kw){
        window.location.href = window.location.pathname + "?search=" + kw;
    } else {
        window.location.href = window.location.pathname;
    }
}