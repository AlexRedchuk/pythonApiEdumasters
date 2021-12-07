from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from EmailApp.models import EmailInfo
from EmailApp.serializers import EmailInfoSerializer 

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from ssl import create_default_context

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
        try:
            emailinfo_serializer.save()
            recipient = emailinfo_serializer.validated_data['EmailInfoUserEmail']
            message = MIMEMultipart("alternative")
            message["Subject"] = "Edumastery"
            message["From"] = "edumasters.team@gmail.com"
            message["To"] = recipient
            message.attach(MIMEText("Thank you for subscribing to our news", "plain"))
            context = create_default_context()
            with SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login("edumasters.team@gmail.com", "edumaster@123")
                server.sendmail("edumasters.team@gmail.com", recipient, message.as_string())
            return JsonResponse("Added Successfully",safe=False)
        except Exception as e:
            print(e)
           
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