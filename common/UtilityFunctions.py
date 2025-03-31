from django.http import HttpResponse
from django.contrib import messages
import json

def toastTrigger(request, status = 204, message = "", toast_style = "success", triggers_to_append = None):
    match toast_style:
        case "success":
            messages.success(request, message)
        case "warning":
            messages.warning(request, message)
        case "error":
            messages.error(request, message)
        case "info":
            messages.info(request, message)

    if triggers_to_append is None:
        triggers_to_append = []

    merged_triggers = {
        key: val 
        for t in triggers_to_append 
        for key, val in t.items()
    }
            
    return HttpResponse(status=status,
            headers={
                'HX-Trigger': json.dumps(merged_triggers)
            }
    )