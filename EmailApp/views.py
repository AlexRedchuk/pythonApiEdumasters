from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from EmailApp.models import EmailInfo
from EmailApp.serializers import EmailInfoSerializer 
from django.core.mail import send_mail


from django.core.files.storage import default_storage

# Create your views here.

@csrf_exempt
def emailInfoApi(request,id=0):
    if request.method=='GET':
        emailinfo = EmailInfo.objects.all()
        emailinfo_serializer=EmailInfoSerializer(emailinfo,many=True)
        return JsonResponse(emailinfo_serializer.data,safe=False)
    elif request.method=='POST':
        emailinfo_data=JSONParser().parse(request)
        emailinfo_serializer=EmailInfoSerializer(data=emailinfo_data)
        if emailinfo_serializer.is_valid():
            send_mail(
                'Subject here',
                'Here is the message.',
                'edumasters.team@gmail.com',
                ['sanya.redchuk@gmail.com'],
                fail_silently=False,
            )
            emailinfo_serializer.save()
            return JsonResponse("Added Successfully",safe=False)
        return JsonResponse("Failed to Add",safe=False)
    elif request.method=='PUT':
        emailinfo_data=JSONParser().parse(request)
        emailinfo=EmailInfo.objects.get(EmailInfoId=emailinfo_data['EmailInfoId'])
        emailinfo_serializer=EmailInfoSerializer(emailinfo,data=emailinfo_data)
        if emailinfo_serializer.is_valid():
            emailinfo_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        emailinfo=EmailInfo.objects.get(EmailInfoId=id)
        emailinfo.delete()
        return JsonResponse("Deleted Successfully",safe=False)


@csrf_exempt
def SaveFile(request):
    file=request.FILES['file']
    file_name=default_storage.save(file.name,file)
    return JsonResponse(file_name,safe=False)