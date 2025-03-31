function createToast(message) {
    const element = htmx.find("[data-toast-template]").cloneNode(true)
  
    delete element.dataset.toastTemplate
  
    element.className += " " + message.tags
  
    htmx.find(element, "[data-toast-body]").innerText = message.message
  
    htmx.find("[data-toast-container]").appendChild(element)
  
    const toast = new bootstrap.Toast(element, { delay: 2000 })
    toast.show()
  }  

htmx.on("messages", (e) => {
    e.detail.value.forEach(createToast)
})