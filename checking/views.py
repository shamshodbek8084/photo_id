from django.shortcuts import render
from .models import Citizen
from .forms import FaceUploadForm
import os
from deepface import DeepFace
from django.conf import settings
from PIL import Image
import uuid

def recognize_face(request):
    result = None
    not_found = False

    if request.method == 'POST':
        form = FaceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Yuklangan rasmni vaqtincha saqlaymiz
            uploaded_file = request.FILES['image']
            filename = f"{uuid.uuid4()}.jpg"
            uploaded_path = os.path.join(settings.MEDIA_ROOT, 'temp', filename)

            os.makedirs(os.path.dirname(uploaded_path), exist_ok=True)
            with open(uploaded_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Ma'lumotlar bazasidagi barcha rasm fayllarini ro'yxatga olamiz
            database_path = os.path.join(settings.MEDIA_ROOT, 'faces')
            try:
                df = DeepFace.find(img_path=uploaded_path, db_path=database_path, enforce_detection=False)

                if len(df) > 0:
                    # Topilgan fayl nomidan Person modelini izlaymiz
                    matched_file = df.iloc[0]['identity']
                    matched_name = os.path.basename(matched_file)
                    person = Citizen.objects.filter(image__icontains=matched_name).first()
                    if person:
                        result = person
                    else:
                        not_found = True
                else:
                    not_found = True

            except Exception as e:
                print("Xatolik:", e)
                not_found = True

    else:
        form = FaceUploadForm()

    return render(request, 'recognizer/index.html', {
        'form': form,
        'result': result,
        'not_found': not_found
    })
