window.onload = (event) => {
    let modals = ['membersModal', 'teamsModal'];
    modals.forEach((modalId) => {
        let md = new bootstrap.Modal(document.getElementById(modalId));
        let dialogId = document.getElementById(modalId).children[0].id;

        htmx.on("htmx:afterSwap", (e) => {
            if (e.detail.target.id == dialogId) {
            md.show();
            }
        })
        
        htmx.on("htmx:beforeSwap", (e) => {
            if (e.detail.target.id == dialogId && !e.detail.xhr.response) {
                md.hide();
                e.detail.shouldSwap = false;
            }
        })
        
        htmx.on("hidden.bs.modal", () => {
            document.getElementById("membersDialog").innerHTML = "";
        })
    });
};