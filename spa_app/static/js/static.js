function search(status) {
    let kw = document.getElementById("search").value.trim();
    let params = new URLSearchParams();

    if (status) {
        params.set("status", status);
    }

    params.set("page", 1);

    if (kw) {
        params.set("search", kw);
    }


    let query = params.toString();
    window.location.href = window.location.pathname + (query ? "?" + query : "");
}
