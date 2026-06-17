import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import FarmerForm
from .models import FarmerTicket, FarmerConsignmentInfo, PaddyInfo


def home(request):
    farmers = FarmerTicket.objects.all()
    paddy_data = PaddyInfo.objects.all()
    farmer_metadata = [col.verbose_name for col in farmers.model._meta.fields]

    if request.method == "POST":
        ticket_id = request.POST.get("ticket_id")
        if ticket_id:
            try:
                farmer = FarmerTicket.objects.get(tracking_id=ticket_id)
                consignment = FarmerConsignmentInfo.objects.filter(tracking_id=farmer).first()
                return render(request, "farmers/track_ticket.html", {
                    "farmer": farmer,
                    "consignment": consignment,
                })
            except FarmerTicket.DoesNotExist:
                pass

    return render(request, "farmers/index.html", {
        "pending_farmers": farmers.exclude(status=FarmerTicket.Status.TRANSPORTED),
        "happy_farmers": farmers.filter(status=FarmerTicket.Status.TRANSPORTED),
        "farmer_metadata": farmer_metadata,
        "paddy_data": paddy_data,
    })


@csrf_exempt
@require_POST
def decode_aadhaar_qr(request):
    from pyaadhaar.decode import AadhaarOldQr, AadhaarSecureQr

    try:
        body = json.loads(request.body)
        qr_text = body.get("qr_text", "").strip()
        if not qr_text:
            return JsonResponse({"success": False, "error": "No QR text provided"})

        try:
            obj = AadhaarOldQr(qr_text)
            result = obj.decodeddata()
            return JsonResponse({
                "success": True,
                "name": result.get("name", ""),
                "aadhar_num": result.get("uid", ""),
                "location": (
                    result.get("vtc")
                    or result.get("dist")
                    or result.get("loc")
                    or ""
                ),
            })
        except Exception:
            pass

        try:
            obj = AadhaarSecureQr(int(qr_text))
            result = obj.decodeddata()
            last_four = result.get("referenceid", "")[:4]
            parts = [
                result.get("house", ""),
                result.get("street", ""),
                result.get("location", ""),
                result.get("vtc", ""),
                result.get("subdistrict", ""),
                result.get("district", ""),
                result.get("state", ""),
                result.get("pincode", ""),
            ]
            address = ", ".join(p for p in parts if p)
            return JsonResponse({
                "success": True,
                "name": result.get("name", ""),
                "aadhar_num": f"****{last_four}" if last_four else "",
                "location": address,
            })
        except Exception:
            pass

        return JsonResponse({"success": False, "error": "Could not decode Aadhaar QR"})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


# Book tickets by farmers for packing paddy
def book_ticket(request):
    if request.method == "POST":
        form = FarmerForm(request.POST)
        if form.is_valid():
            ticket = form.save()

            return HttpResponse("thanks")
    else:
        form = FarmerForm()

    return render(request, "farmers/book_ticket.html", {"form": form})


