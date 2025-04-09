window.onload = (event) => {
    let modals = ['membersModal', 'teamsModal', 'userModal'];
    modals.forEach((modalId) => {

        if(document.getElementById(modalId)) {
            
            let md = new bootstrap.Modal(document.getElementById(modalId));
            let dialogId = document.getElementById(modalId).children[0].id;
            
            htmx.on("htmx:afterSwap", (e) => {
                if (e.detail.target.id == dialogId) {
                    md.show();
                }
            })
            
            htmx.on("htmx:beforeSwap", (e) => {
                if (e.detail.target.id == dialogId && !e.detail.xhr.response || e.detail.target.classList.contains("team") || e.detail.target.classList.contains("profile")) {
                    md.hide();
                    if(e.detail.target.classList.contains("team") || e.detail.target.classList.contains("profile")) {
                        e.detail.shouldSwap = true;
                    }else{
                        e.detail.shouldSwap = false;
                    }
                }
            })
            
            htmx.on("hidden.bs.modal", () => {
                document.getElementById(dialogId).innerHTML = "";
            })

        }

    });
};