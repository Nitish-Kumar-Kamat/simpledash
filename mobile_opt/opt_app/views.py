import requests
from django.shortcuts import render
import random
from django.http import HttpResponse

def send_otp_sms(mobile, otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    headers = {
        'authorization': 'tFCQiYPBVUuRhKmE4p1WHsaNwD8JqZTkog9rSndzv0L7Gxe3f5Ysd7CrDpHP3VmenyTUjJGhEoIuR8gi',
        'Content-Type': 'application/json'
    }
    payload = {
        "route": "otp",
        "message": f"Your OTP is {otp}",
        "language": "english",
        "numbers": mobile,
    }

    response = requests.post(url, headers=headers, json=payload)
    print("Response:", response.text)
    return response.json()




def send_otp_view(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        otp = random.randint(100000, 999999)

        # Save OTP in session (or DB)
        request.session['otp'] = str(otp)
        request.session['mobile'] = mobile

        send_otp_sms(mobile, otp)
        return render(request, 'verify_otp.html', {'mobile': mobile})

    return render(request, 'send_otp.html')




def verify_otp_view(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        real_otp = request.session.get('otp')

        if user_otp == real_otp:
            return HttpResponse("✅ OTP Verified Successfully!")
        else:
            return HttpResponse("❌ Invalid OTP. Please try again.")

    return HttpResponse("Bad Request")
