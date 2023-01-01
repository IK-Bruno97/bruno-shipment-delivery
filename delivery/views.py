from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
import random, math
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from validate_email import validate_email
from django.contrib import messages
from .models import Shipment

#from django.views.decorators.cache import cache_page

# Create your views here.

#@cache_page(60 * 15)
def home(request):
    return render(request, 'delivery/home.html')

def reg_no():
    str = 'ABCDEFXYZ'
    number = '012345679'
    string = str + number 
    registration_number = ""
    length = len(string)
    for i in range(8):
        registration_number += string[math.floor(random.random() * length)]
    return registration_number


def tracking_number():
    str = 'ABCDEFXYZ'
    number = '012345679'
    symbol = "ijklmnpqst"
    string = str + number + symbol
    tracking_number = ""
    length = len(string)
    for i in range(10):
        tracking_number += string[math.floor(random.random() * length)]
    return tracking_number


class ShipmentView(View):
    def get(self, request):
        return render(request, 'delivery/shipment.html')

    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False,
        }
        
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        package = request.POST.get('package')
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        weight = request.POST.get('weight')

        tracking = tracking_number()
        registration_number = reg_no()
        try:
            if not validate_email(email):
                messages.add_message(request, messages.ERROR,
                                    'Please provide a valid email')
                context['has_error'] = True
                
        except Exception as identifier:
            pass

        if context['has_error']:
            return render(request, 'delivery/shipment.html', context, status=400)


        else:
            ToShip = Shipment.objects.create(
                email=email,
                full_name=full_name,
                phone=phone,
                package=package,
                origin=origin,
                destination=destination,
                weight=weight,
                tracking_number=tracking
            )
            ToShip.save()
            

            
            mail_subject = 'Shipment Delivery Details.'
            message = render_to_string('delivery/emailconfirmation.html', {
                'full_name': full_name,
                'registration_number': registration_number,
                'tracking_number': tracking,
            })
            to_email = email
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
           
        return HttpResponse('<center>Shipment recieved with registration number: ' + registration_number + '. Confirm your mail inbox for your tracking number and payment information. <a href="/">Back</a></center>')


class TrackingView(View):
    def get(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }
        tracking = request.POST.get('tracking')

        try:
            if Shipment.objects.get(tracking_number=tracking):
                return render(request, 'delivery/tracking.html')

        except Exception as identifier:
            messages.add_message(request, messages.ERROR, 'Invalid tracking number')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'delivery/home.html', context, status=400)
            

    def post(self, request):
        if request.method == "POST":
            tracking = request.POST['tracking']
            try:
                ship = Shipment.objects.get(tracking_number=tracking)
                name = ship.full_name
                destination = ship.destination
                package = ship.package
                shipment_day = ship.date.strftime("%w")
                shipment_date = ship.date.strftime("%d")
                shipment_month = ship.date.strftime("%m")
                shipment_year = ship.date.strftime("%Y")

                datestr = ship.date.strftime("%d:%m:%Y")
                bgdate = datetime.strptime(datestr, "%d:%m:%Y")
                delivery_date = bgdate + timedelta(days=2)
                
                return render(request, 'delivery/tracking.html', {'name':name,
                    'destination':destination,
                    'package': package,
                    'shipment_date': shipment_date,
                    'shipment_day': shipment_day,
                    'shipment_month': shipment_month,
                    'shipment_year': shipment_year,
                    'delivery_date': delivery_date,
                })
            except Exception as identifier:
                return render(request, "delivery/home.html", {"message": "Invalid tracking id!"})
               
        
