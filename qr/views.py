from django.shortcuts import render
from django.http import HttpResponse
import qrcode
from io import BytesIO

def generar_qr(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)

            img = qr.make_image(fill='black', back_color='white')
            buffer = BytesIO()
            img.save(buffer)
            buffer.seek(0)
            
            return HttpResponse(buffer, content_type='image/png')
    return render(request, 'qr/index.html')
