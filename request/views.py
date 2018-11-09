# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import request as table
from forms import createRequest
from django.utils.crypto import get_random_string
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from email.mime.base import MIMEBase 
from email import encoders 
from DARequest import settings
import re

bd = settings.BASE_DIR
# Create your views here.

def send_mail_attachment(send_from, send_to,cc_email, subject, text, files):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['CC'] = cc_email
    msg['Subject'] = subject

    msg.attach(MIMEText(text))
    filename = re.sub(r"^.*?/sendfiles/", r"", files)
    attachment = open(files, "rb")
    p = MIMEBase('application', 'octet-stream') 
    p.set_payload((attachment).read()) 
    encoders.encode_base64(p) 
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    msg.attach(p) 
    smtp = smtplib.SMTP('202.129.198.133', 25,timeout=30)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


def Mailsend(subject, Message, emailfrom, emailto, cc_email):
    User_name = emailfrom
    Password  = "algolitics"
    cc        = [cc_email]
    fromaddr  = 'postmaster365@algolitics.in'
    message = "From: %s\r\n" % fromaddr + "To: %s\r\n" % emailto + "CC: %s\r\n" % ",".join(cc) + "Subject: %s\r\n" % subject + "\r\n" + Message
    toaddrs = [emailto] + cc 
    server = smtplib.SMTP('202.129.198.133',25,timeout=30)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(User_name,Password)
    server.sendmail(fromaddr, toaddrs, message)
    server.quit()
    

def newrequest(request):
    if request.method == "POST":
        if "requestorempid" in request.POST:
            post = request.POST.copy()
            unique_id = get_random_string(length=8)
            post['requestid'] = unique_id
            post['excepted_TAT'] = post['excepted_TAT_0']+' '+post['excepted_TAT_1']+':00'
            post.pop('excepted_TAT_0')
            post.pop('excepted_TAT_1')
            form = createRequest(post, request.FILES)
            if form.is_valid():
                model_instance = form.save(commit=False)
                model_instance.save()
                ids= model_instance.pk
                updatedata = table.objects.get(id = ids)
                rid =  'DAR'+str(ids)
                updatedata.requestid = rid
                updatedata.save()
                subject = str("DA RequestID: ")+rid+'_'+str(post['processoverview'])
                emailfrom = 'postmaster365@algolitics.in' 
                #receiver = 'eswaram@algolitics.in', 'maruthupandianp@algolitics.in', 'jayaprakashs@algolitics.in', 'perumaals@algolitics.in'
                receiver = 'eswaram@algolitics.in', 'maruthupandianp@algolitics.in'
                emailto =  ','.join(receiver)
                #receivercc = [str(post['requestormanagermailid']), str(post['requestormailid']), 'sujaik@algolitics.in']
                receivercc = [str(post['requestormanagermailid']), str(post['requestormailid'])]
                cc_email = ','.join(receivercc)
                if request.FILES.has_key('document'):
                    sendfile = bd+'/media/sendfiles/'+str(request.FILES['document'].name)
                    with open(bd+'/media/sendfiles/'+str(request.FILES['document'].name), 'wb+') as destination:
                        for chunk in request.FILES['document'].chunks():
                            destination.write(chunk)
                    Message = """
Hi Team,
                                
We have received a new request from {0}
                                
Project - {1}
Process - {2}
Expected TAT - {3}
Request Overview - {4} 
Request Details - {5}

Note: Supporting document attached. 

With Regards,
DA Team
""".format(str(post['requestorname']), str(post['projectname']), str(post['process']),  datetime.datetime.strptime(str(post['excepted_TAT']), "%Y-%m-%d %H:%M:%S").strftime("%b.%d,%Y,%I:%M %p"),post['processoverview'],post['description'] )
                    send_mail_attachment(emailfrom, emailto,cc_email,subject, Message, sendfile)
                else:
                    Message = """
We have received a new request from {0}
                                
Project - {1}
Process - {2}
Expected TAT - {3}
Request Overview - {4} 
Request Details - {5}

With Regards,
DA Team
""".format(str(post['requestorname']), str(post['projectname']), str(post['process']),  datetime.datetime.strptime(str(post['excepted_TAT']), "%Y-%m-%d %H:%M:%S").strftime("%b.%d,%Y,%I:%M %p"),post['processoverview'],post['description'] )
                    Mailsend(subject, Message, emailfrom, emailto, cc_email)
                
                return render(request, "index2.html", {'Requestid': rid})
            else:
                print "Not valid"
        if "searchrequestid" in request.POST:
            rid = request.POST['searchrequestid']
            search = table.objects.values("requestid", "requestorname", "requesteddate", "projectname", "process", "excepted_TAT", "status", "comments").filter(requestid = rid)
            return render(request, "index3.html", {'data': search})
    else:
        form = createRequest()
    return render(request, "index.html", {'form': form})