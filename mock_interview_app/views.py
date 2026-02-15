import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from mock_interview_app.models import *


def log(request):

    return render(request,"login_index.html")

def login_post(request):
    uname=request.POST['username']
    pwd=request.POST['password']
    data=login_tb.objects.filter(username=uname,password=pwd)

    if data.exists():
        ldata=data[0]
        request.session['count'] = 0
        request.session['lid']=ldata.id
        if ldata.usertype=='admin':
            return HttpResponse("<script>alert('Login Success');window.location='/admin_home'</script>")
        if ldata.usertype=='company':
            request.session['lid'] = ldata.id
            request.session['uid'] = company_tb.objects.get(LOGIN=request.session['lid']).id
            return HttpResponse("<script>alert('Login Success');window.location='/company_home'</script>")
        elif ldata.usertype=='user':
            request.session['lid'] = ldata.id
            request.session['uid'] = user_tb.objects.get(LOGIN=request.session['lid']).id
            # request.session['candidate_id'] = candidate_tb.objects.get(USER=request.session['uid']).id
            return HttpResponse("<script>alert('Login Success');window.location='/user_home'</script>")
        else:
            return HttpResponse("<script>alert('Invalid User');window.location='/'</script>")

    else:

        return HttpResponse("<script>alert('Data Not Found');window.location='/';</script>")


def admin_home(request):
    return render(request,"Admin/index.html")

def approved_company(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head'] = "VIEW APPROVED COMPANY"
    ress=company_tb.objects.filter(LOGIN__usertype='company')
    return render(request,"Admin/view approved company.html",{'data':ress})

def company_and_approve(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head'] = "VIEW COMPANY"
    res=company_tb.objects.filter(LOGIN__usertype='pending')
    return render(request,"Admin/view company and approve.html",{'data':res})

def approve_company(request,id):
    login_tb.objects.filter(id=id).update(usertype='company')
    import smtplib
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("interviewmock123@gmail.com ", "ehok fmsl tvwk qtcr")
    msg = MIMEMultipart()  # create a message.........."
    msg['From'] = "interviewmock123@gmail.com"
    msg['To'] = login_tb.objects.get(id=id).username
    msg['Subject'] = "you are approved"
    body = "you are apprioved"
    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)



    return HttpResponse("<script>alert('approved');window.location='/company_and_approve#aa';</script>")


def reject_company(request,id):
    login_tb.objects.filter(id=id).update(usertype='reject')
    import smtplib
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("interviewmock123@gmail.com ", "tzsj bmpy sbrj elmb")
    msg = MIMEMultipart()  # create a message.........."
    msg['From'] = "interviewmock123@gmail.com"
    msg['To'] = login_tb.objects.get(id=id).username
    msg['Subject'] = "you are Rejected"
    body = "you are Rejected"
    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)

    return HttpResponse("<script>alert('rejected');window.location='/company_and_approve#aa';</script>")



def company_review(request,id):

    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head'] = "VIEW REVIEW"
    res=review_tb.objects.filter(COMPANY_id=id)
    return render(request,"Admin/view company review.html",{'data':res})

def placed_candidates(request):

    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head'] = "placed candidates"
    res = candidate_tb.objects.filter(status='selected')
    return render(request,"Admin/view placed candidates.html",{'data':res})

def rejected_company(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head'] = "Rejected Company"
    res = company_tb.objects.filter(LOGIN__usertype='reject')
    return render(request,"Admin/view reject company.html",{'data':res})

def vaccency_list(request,id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head'] = "VIEW VACCANCY LIST"
    resss=vacancy_tb.objects.filter(COMPANY_id=id)
    return render(request,"Admin/view vaccency list.html",{'data':resss})


#----------------------------------------------------------------------------------

def change_password(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head']="Change Password"
    return render(request,"company/change password.html")

def change_password_post(request):
    c_password = request.POST['cpass']
    n_password=request.POST['npass']
    confirm_password=request.POST['cmpass']

    data=login_tb.objects.filter(password=c_password,usertype="company",id=request.session['lid'])
    if data.exists():
        if n_password==confirm_password:
            login_tb.objects.filter(id=request.session['lid']).update(password=confirm_password)
            return HttpResponse("<script>alert('password changed');window.location='/';</script>")

        else:
            return HttpResponse("<script>alert('password missmatch');window.location='/change_password';</script>")


    return HttpResponse("<script>alert('not found');window.location='/change_password';</script>")



def compay_home(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head'] = " "
    return render(request,"company/index.html")

def company_reg(request):
    return render(request,"company/company.html")

def company_reg_post(request):
    u_name = request.POST['name']
    u_email = request.POST['email']
    u_contact = request.POST['contact']
    u_lisence = request.FILES['lis']
    fs = FileSystemStorage()
    d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fs.save(r"C:\Users\user\Downloads\real_time_mock_interview\real_time_mock_interview\mock_interview_app\static\image\\" + d + ".pdf",
            u_lisence)
    path2 = "/static/image/" + d + ".pdf"

    u_image = request.FILES['img']
    fs=FileSystemStorage()
    d=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fs.save(r"C:\Users\user\Downloads\real_time_mock_interview\real_time_mock_interview\mock_interview_app\static\image\\"+d+  ".jpg",u_image)
    path="/static/image/" +d+".jpg"

    u_latitude = request.POST['lat']
    u_longitude = request.POST['long']
    u_password = request.POST['pass']
    u_confirm_password = request.POST['cpass']
    if u_password==u_confirm_password:

        obj1=login_tb()
        obj1.username=u_email
        obj1.password=u_confirm_password
        obj1.usertype="pending"
        obj1.save()


        obj = company_tb()
        obj.name = u_name
        obj.email = u_email
        obj.contact = u_contact
        obj.lisence = path2
        obj.image = path
        obj.latitude = u_latitude
        obj.longitude =u_longitude
        obj.LOGIN_id=obj1.id

        obj.save()
        return HttpResponse("<script>alert('Registered Success');window.location='/'</script>")
    else:
        return HttpResponse("<script>alert('password missmatch');window.location='/company_reg'</script>")




# def edit_profile(request):
#     if request.session['lid'] == '':
#         return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
#     request.session['head'] = "Edit Profile"
#     return render(request,"company/edit profile.html")
#
# def edit_profile_post(request):
#     u_name=request.POST['textfield']
#     u_email=request.POST['textfield2']
#     u_contact=request.POST['textfield3']
#     u_lisence=request.POST['textfield4']
#     u_image=request.POST['filefield']




def edit_question(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head'] = "Edit Question"
    rdate = datetime.datetime.now().strftime("%Y-%m-%d")
    return render(request,"company/edit question.html",{"rdate":rdate})

def edit_question_post(request):
    u_question = request.POST['textarea']
    u_optionA = request.POST['textfield']
    u_optionB = request.POST['textfield2']
    u_optionC = request.POST['textfield3']
    u_optionD = request.POST['textfield4']
    u_correct_ans = request.POST['select']

def edit_vacancy(request,id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head'] = "Edit Vacency"
    data=vacancy_tb.objects.get(id=id)
    rdate = datetime.datetime.now().strftime("%Y-%m-%d")
    return render(request,"company/edit vacency.html",{'data':data,"rdate":rdate})

def edit_vacancy_post(request,id):
    u_vacancy = request.POST['type']
    u_job_title = request.POST['title']
    u_job_requirement = request.POST['re']
    u_applydate = request.POST['date']
    u_salary =request.POST['salery']
    vacancy_tb.objects.filter(id=id).update(vacancy_type=u_vacancy,job_title=u_job_title,job_requirement=u_job_requirement,apply_date=u_applydate,salary=u_salary)
    return HttpResponse("<script>alert('edit sucessfully');window.location='/view_vacency'</script>")

def question_add(request,id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head'] = "Add Question"
    return render(request,"company/question add.html",{"id":id})

def question_add_post(request,id):
    u_question = request.POST['textarea']
    option_1 = request.POST['textfield']
    option_2 = request.POST['textfield2']
    option_3 = request.POST['textfield3']
    option_4 = request.POST['textfield4']
    answer = request.POST['RadioGroup1']

    data = question_tb.objects.filter(question=u_question, VACENCY_id=id)
    if data.exists():
        return HttpResponse('<script>alert("Already added");window.location="/question_add#aa"</script>')
    else:
        if answer == 'A':
            ans = option_1
            print("ans", ans)
        elif answer == 'B':
            ans = option_2
            print("ans", ans)
        elif answer == 'C':
            ans = option_3
            print("ans", ans)
        elif answer == 'D':
            ans = option_4
            print("ans", ans)

        obj = question_tb()
        obj.answers = answer
        obj.option_A = option_1
        obj.option_B = option_2
        obj.option_C = option_3
        obj.option_D = option_4
        obj.answer = ans
        obj.VACENCY_id= id
        obj.question = u_question
        obj.save()
        return HttpResponse("<script>alert('added sucess');window.location='/question_add/"+id+"#aa'</script>")




def vacancy(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head'] = "ADD VACANCY"
    rdate = datetime.datetime.now().strftime("%Y-%m-%d")
    return render(request,"company/vacancy.html",{"rdate":rdate})

def vacancy_post(request):
    u_vacancy = request.POST['type']
    u_job_title = request.POST['title']
    u_job_requirement = request.POST['re']
    u_applydate = request.POST['date']
    u_cuttoff = request.POST['cutoff']

    u_salary =request.POST['salery']

    obj = vacancy_tb()
    obj.vacancy_type = u_vacancy
    obj.job_title = u_job_title
    obj.job_requirement = u_job_requirement
    obj.apply_date = u_applydate
    obj.salary = u_salary
    obj.cuttoff = u_cuttoff
    obj.COMPANY= company_tb.objects.get(LOGIN=request.session['lid'])

    obj.save()
    return HttpResponse("<script>alert('added sucess');window.location='/view_vacency#aa';</script>")






def view_vacency(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head'] = "View Vacency "
    data=vacancy_tb.objects.filter(COMPANY__LOGIN=request.session['lid'])
    return render(request,"company/view_vacancy.html",{"data":data})


def delete_vacency(request,id):
   vacancy_tb.objects.filter(id=id).delete()
   return HttpResponse("<script>alert('delete sucess');window.location='/view_vacency';</script>")


def view_candidates(request,id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head'] = "View Candidates "
    data=candidate_tb.objects.filter(VACENCY=id)
    return render(request,"company/view candidate.html",{"data":data})

def view_profile(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head'] = "View Profile "
    data = company_tb.objects.get(LOGIN = request.session['lid'])
    return render(request,"company/view profile.html",{"data":data})


def edit_profile_update(request,id):
    u_name = request.POST['textfield']
    u_email = request.POST['textfield2']
    u_contact = request.POST['textfield3']
    u_latitude= request.POST['latitude']
    u_longitude= request.POST['longitude']
    company_tb.objects.filter(id=id).update(name=u_name, email=u_email, contact=u_contact, latitude=u_latitude, longitude=u_longitude)

    if 'img' in request.FILES:
        u_image = request.FILES['img']
        fs = FileSystemStorage()
        d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        fs.save(r"C:\Users\user\Downloads\real_time_mock_interview\real_time_mock_interview\mock_interview_app\static\image\\" + d + ".jpg",u_image)
        path1 = "/static/image/" + d + ".jpg"
        company_tb.objects.filter(id=id).update(image=path1)
    if 'lis' in request.FILES:
        u_lisence = request.FILES['lis']
        fs = FileSystemStorage()
        d = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        fs.save(r"C:\Users\user\Downloads\real_time_mock_interview\real_time_mock_interview\mock_interview_app\static\image\\" + d + ".pdf",u_lisence)
        path = "/static/image/" + d + ".pdf"
        company_tb.objects.filter(id=id).update(lisence=path)
    return HttpResponse("<script>alert('edit sucess');window.location='/view_profile#aa';</script>")


def view_question(request,id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head'] = "Question "
    res = question_tb.objects.filter(VACENCY_id=id)
    return render(request,"company/view question.html",{"data":res})

def logout(request):
    return HttpResponse("<script>alert('logout sucess');window.location='/';</script>")


# def schedule_test(request,id):
#     if request.session['lid'] == '':
#         return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
#     return render(request, "company/schedule test.html",{"id":id})
#
#
# def schedule_test_post(request,id):
#     date=request.POST['textfield']
#     time=request.POST['textfield2']
#     candidate_tb.objects.filter(USER_id=id).update(exam_date=date,exam_time=time)
#     return HttpResponse("<script>alert('test scheduled');window.location='/company_home';</script>")

def view_shortlist_candidates(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    # short=exam_tb.objects.filter(CANDIDATE__VACENCY_id=id)
    request.session['head'] = "View Shortlist Candidates "
    short=candidate_tb.objects.filter(status__in=['shortlisted','scheduled'])
    print("shorrttttttttttttttttt",short)

    return render(request, "company/shortlist candidates.html",{'data':short})

def schedule_interview(request,id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head'] = "SCHEDULE INTERVIEW"
    rdate = datetime.datetime.now().strftime("%Y-%m-%d")
    return render(request, "company/schedule interview.html",{'id':id,"rdate":rdate})


def schedule_interview_post(request,id):
    date=request.POST['textfield']
    time=request.POST['textfield2']
    candidate_tb.objects.filter(id=id).update(interview_date=date,interview_time=time)

    return HttpResponse("<script>alert('interview time scheduled');window.location='/company_home';</script>")


def mark_candidates(request,id):
    candidate_tb.objects.filter(USER_id=id).update(status='selected')

    return HttpResponse("<script>alert('candidates marked');window.location='/company_home';</script>")


def edit_questions(request,id):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    qst= question_tb.objects.get(id=id)
    return render(request,"company/edit question.html",{'data':qst})


def edit_questions_post(request,id):
    q = question_tb.objects.get(id = id)

    v = str(q.VACENCY_id)

    d=request.POST['textarea']
    e=request.POST['textfield']
    g=request.POST['textfield2']
    h=request.POST['textfield3']
    i=request.POST['textfield4']
    j=request.POST['select']

    question_tb.objects.filter(id=id).update(answer=d, question=e,option_A=g,option_B=h,option_C=i,option_D=j)

    return HttpResponse("<script>alert('edited sucess');window.location='/view_question/"+v+"';</script>")

def delete_question(request,id):
    q = question_tb.objects.get(id = id)
    v = str(q.VACENCY_id)
    q.delete()
    return HttpResponse("<script>alert('delete sucess');window.location='/view_question/"+v+"';</script>")






















#------------------------


def chatt(request,u):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head']="CHAT"
    request.session['uid'] = u
    print("GGG  ", u)
    return render(request,'company/chat.html',{'u':u})


def chatsnd(request):
    d=datetime.datetime.now().strftime("%Y-%m-%d")
    # t=datetime.datetime.now().strftime("%H:%M:%S")
    c = request.session['lid']
    b=request.POST['n']
    print(b)
    m=request.POST['m']
    cc = company_tb.objects.get(LOGIN=request.session['lid'])
    print(c,"ccccccccccc")
    # cc=1
    uu = user_tb.objects.get(id=request.session['uid'])
    print(uu,"customer_id")
    print("cccccc",cc)
    print("uuuuuuuuuu",uu)
    obj=chat_tb()
    obj.date=d
    obj.type='company'
    obj.COMPANY=cc
    obj.USER=uu
    obj.chat=m
    obj.save()

    print(obj)
    v = {}
    if int(obj) > 0:
        v["status"] = "ok"
    else:
        v["status"] = "error"
    r = JsonResponse.encode(v)
    return r
# else:
#     return redirect('/')

def chatrply(request):
    # if request.session['log']=="lo":
    # c = request.session['lid']
    # rid=request.POST['rid']
    cc=company_tb.objects.get(LOGIN=request.session['lid'])

    # print("JJJJ  ",rid)
    uu=user_tb.objects.get(id=request.session['uid'])
    print("uuuuuuu",uu)
    res = chat_tb.objects.filter(COMPANY=cc,USER=uu)
    print(res)
    v = []
    if len(res) > 0:
        print(len(res))
        for i in res:
            v.append({
                'type':i.type,
                'chat':i.chat,
                'name': "user",

                # 'id':i.CUSTOMERS.id,
                # 'upic':i.USER.photo,
                'dtime':i.date,
                'tname':i.USER.name,
            })
        print(v)
        return JsonResponse({"status": "ok", "data": v})
    else:
        return JsonResponse({"status": "error"})

def change_pswd (request):

    if request.session['lid'] == '':

        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head'] = "CHANGE PASSWORD"
    return render(request, "user/change password.html")

def change_pswd_post(request):
    c_password = request.POST['textfield']
    n_password=request.POST['textfield2']
    confirm_password=request.POST['textfield3']

    data=login_tb.objects.filter(password=c_password,usertype="user",id=request.session['lid'])
    if data.exists():
        if n_password==confirm_password:
            login_tb.objects.filter(id=request.session['lid']).update(password=confirm_password)
            return HttpResponse("<script>alert('password changed');window.location='/';</script>")

        else:
            return HttpResponse("<script>alert('password missmatch');window.location='/change_pswd';</script>")


    return HttpResponse("<script>alert('not found');window.location='/change_pswd';</script>")

def review_company (request,id):
    request.session['head'] = "REVIEW"
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    return render(request, "user/review_company.html", {"id": id})

def review_post (request,id):
    rev=request.POST['textarea']
    d=datetime.datetime.now()
    obj=review_tb()
    obj.review=rev
    obj.date=d
    obj.COMPANY_id=id
    obj.USER_id=user_tb.objects.get(LOGIN=request.session['lid']).id
    obj.save()

    return HttpResponse("<script>alert('review send');window.location='/user_home';</script>")


def user_home (request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    return render(request, "user/index.html")

def user_login(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    return render(request, "user/user login.html")

def signup (request):
    return render(request, "user/useer_registerpage.html")

def signup_post (request):
    nm=request.POST['textfield']




    im=request.FILES['fileField']
    d=datetime.datetime.now().strftime("%d%m%Y-%H%M%S")
    fs=FileSystemStorage()
    fs.save(r"C:\Users\user\Downloads\real_time_mock_interview\real_time_mock_interview\mock_interview_app\static\image\\"+d+'.jpg',im)
    p="/static/image/"+d+'.jpg'

    plc=request.POST['textfield2']
    pinn=request.POST['textfield3']
    pst=request.POST['textfield4']
    eml=request.POST['textfield5']
    cnt=request.POST['textfield6']
    lat=request.POST['textfield7']
    lon=request.POST['textfield8']
    pss=request.POST['textfield9']
    cpss=request.POST['textfield10']
    if pss==cpss:
        obj=login_tb()
        obj.username=eml
        obj.password=pss
        obj.usertype="user"
        obj.save()

        ob=user_tb()
        ob.name=nm
        ob.image=p
        ob.place=plc
        ob.pin=pinn
        ob.post=pst
        ob.email=eml
        ob.contact=cnt
        ob.latitude=lat
        ob.longitude=lon
        ob.longitude=lon
        ob.LOGIN=obj
        ob.save()
        return HttpResponse("<script>alert('signup sucessfull');window.location='/log';</script>")
    else:
        return HttpResponse("<script>alert('signup failed');window.location='/signup';</script>")





def view_profilee(request):
    request.session['head'] = "VIEW PROFILE"
    data = user_tb.objects.get(LOGIN=request.session['lid'])
    return render(request, "user/user view profile.html", {"data": data})


def view_company(request):
    request.session['head'] = "VIEW COMPANY"
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    data=company_tb.objects.filter(LOGIN__usertype='company')
    return render(request, "user/view _company.html", {"data": data})





def final_result(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head'] = "FINAL RESULT"
    data = candidate_tb.objects.filter(USER__LOGIN=request.session['lid'],status='selected')
    return render(request, "user/view_final_result.html", {"data": data})


# def schedule_list(request):
#     if request.session['lid'] == '':
#         return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
#     data = candidate_tb.objects.filter()
#     return render(request, "user/view_scheduled_list.html", {"data": data})


# def short_list(request,id):
#     if request.session['lid'] == '':
#         return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
#     data= candidate_tb.objects.filter(VACENCY__COMPANY=id,status='shortlisted')
#     return render(request, "user/view_short_list.html", {"data": data})

def view_vacancy(request,id):
    request.session['cid']=id
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    data= vacancy_tb.objects.filter(COMPANY=id)
    return render(request, "user/view_vacency.html", {"data": data})


def apply_vacency(request,id):
    cid=request.session['cid']
    res=candidate_tb.objects.filter(VACENCY_id=id,USER__LOGIN=request.session['lid'])
    if res.exists():
        return HttpResponse("<script>alert('already applied');window.location='/view_vacancy/"+str(cid)+"';</script>")

    d=datetime.datetime.now()
    obj=candidate_tb()
    obj.VACENCY_id=id
    obj.USER=user_tb.objects.get(LOGIN=request.session['lid'])
    obj.date=d
    obj.status='shortlisted'
    obj.exam_date='pending'
    obj.exam_time='pending'
    obj.interview_date='pending'
    obj.interview_time='pending'
    obj.no_of_unknown_person = 'pending'
    obj.no_of_unknown_person = 'pending'
    obj.save()


    return HttpResponse("<script>alert('applied sucessfull');window.location='/user_home';</script>")


def main_index (request):

    return render(request, "INDEX.html")



def company_view_applied_candidate(request):
    data = candidate_tb.objects.filter(status='selected',VACENCY__COMPANY__LOGIN=request.session['lid'])
    return render(request,"company/view_applied_candidate.html",{"data":data})


# --- SCHEFULE TEST ---

def schedule_test(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "SCHEDULE TEST"
    rdate = datetime.datetime.now().strftime("%Y-%m-%d")
    return render(request,"company/schedule_test.html",{"id":id,"rdate":rdate})

def schedule_test_post(request,id):
    print(id,"ioioioi")
    from datetime import datetime
    exam_date = request.POST['textfield']
    exam_time = request.POST['textfield2']

    exam_time_24 = datetime.strptime(exam_time, "%H:%M")
    exam_time_12 = exam_time_24.strftime("%I:%M")


    candidate_tb.objects.filter(id=id).update(exam_date=exam_date,exam_time=exam_time,status="shortlisted")
    return HttpResponse("<script>alert('Test Scheduled');window.location='/company_view_applied_candidate'</script>")

def view_schedule_test(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "VIEW SCHEDULE TEST"
    data = candidate_tb.objects.filter(id=id)
    return render(request,"company/view_scheduletest.html",{"data":data})















# #--  exam attending --
#
# def view_shortlisted_list(request):
#     if "lid" not in request.session:
#         return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
#     request.session['head'] = "VIEW SHORTLISTED LIST"
#
#     data = user_tb.objects.filter(STUDENT__LOGIN=request.session['lid'],status__in=['shortlisted','updated'])
#     import datetime
#     current_date = datetime.datetime.now().strftime("%Y-%m-%d")
#     current_time = datetime.datetime.now().strftime("%H-%M")
#
#     print("current_date",current_date)
#     print("current_time",current_time)
#
#     data1 = user_tb.objects.filter(interview_date=current_date,interview_time=current_time,STUDENT__LOGIN=request.session['lid'])
#     return render(request,"user/view_shortlisted_list.html",{"data":data,"data1":data1})
#
#
# def view_exam_date(request,id):
#     if "lid" not in request.session:
#         return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
#     request.session['head'] = "VIEW EXAM DATE"
#     request.session['candidate_id'] = id
#     import datetime
#     current_date = datetime.datetime.now().strftime("%Y-%m-%d")
#     current_time_24 = datetime.datetime.now().strftime("%H:%M")
#     current_time_12 = datetime.datetime.strptime(current_time_24, "%H:%M").strftime("%I:%M")
#
#     print("current_dateeeeeeeeeee",current_date)
#     print("current_time_12222222222",current_time_12)
#     data = candidate_tb.objects.get(id=id)
#     data1 = candidate_tb.objects.filter(exam_date=current_date, exam_time=current_time_12)
#     request.session['count'] = 0
#     return render(request,"user/view_exam_date.html",{"data":data,"data1":data1,"current_date":current_date})
#
#
# def submit_answer(request,id):
#
#
#     candidatee = candidate_tb.objects.get(STUDENT__LOGIN=request.session['lid'])
#
#     question_index = int(request.POST.get('index'))
#     selected_answer = request.POST.get('selected_answer')
#
#     res = question_tb.objects.filter(VACCANCY=id).order_by('id')
#     if question_index < 0 or question_index >= len(res):
#         return HttpResponse("<script>alert('Invalid question index');window.location='/submit_answer#aaa'</script>")
#
#     single_question = res[question_index]
#
#     is_correct = (str(selected_answer) == str(single_question.answer))
#     print(selected_answer , single_question.answer,selected_answer == single_question.answer)
#     marks = 1 if is_correct else 0
#
#     res1=exam_tb.objects.filter(CANDIDATE=candidatee)
#     if res1.exists():
#         current_marks = res1[0].mark
#         a = str(int(current_marks) + int(marks))
#         request.session['mark']=a
#         exam_tb.objects.filter(CANDIDATE=candidatee).update(mark=a)
#         cutoff = candidate_tb.objects.get(id=candidatee.id).VACCANCY.cutt_off
#         if int(a) > int(cutoff):
#             candidate_tb.objects.filter(id=candidatee.id).update(status='scheduled')
#         else:
#             candidate_tb.objects.filter(id=candidatee.id).update(status='examattended')
#     else:
#         candidate_result=exam_tb()
#         candidate_result.CANTIDATE=candidatee
#         candidate_result.mark=marks
#         candidate_result.save()
#
#     is_last_question = (question_index == len(res) - 1)
#
#     data = {
#         'status': "ok",
#         'is_last_question': is_last_question
#     }
#
#     return render(request, 'user/view_test_result.html', {'data': data})
#
#
# def view_sample_question(request, id):
#
#     request.session['head'] = "VIEW SAMPLE QUESTION"
#     if request.session.get("lg") != "lin":
#         return HttpResponse("<script>alert('Please login!');window.location='/'</script>")
#
#     data = candidate_tb.objects.filter(id=id)
#
#     if data[0].no_of_unknown_person == 2 and data[0].multiple_person == 2:
#         return HttpResponse("<script>alert('Unauthorised events ocuured..Exam is blocked!!');window.location='/view_exam_date/'"+str(id)+"''</script>")
#
#
#     questions = question_tb.objects.filter(VACCANCY=id)
#     request.session['count'] = request.session.get('count', 0)
#     request.session['testid'] = id
#
#     if request.session['count'] < len(questions):
#         current_question = questions[request.session['count']]
#     else:
#         return HttpResponse("<script>alert('No more questions available!');window.location='/view_shortlisted_list#aaa'</script>")
#
#     ar = {
#         'data': current_question,
#         'c': request.session['count'] + 1
#     }
#
#     return render(request, 'user/attend_exam.html', ar)
#
# # def play_newcam(request):
# #     from newcam import face_detection_and_emotion
# #     # face_detection_and_emotion(request.session['lid'],request.session['candidate_id'])
# #     response = face_detection_and_emotion(request.session['lid'], request.session['candidate_id'])
# #     print("response",response)
# #
# #     return render(request, 'user/attend_exam.html',{'response': response})
#
# def play_newcam(request):
#     from newcam import face_detection_and_emotion  # Importing the function correctly
#     try:
#         # Call the emotion detection function
#         response = face_detection_and_emotion(request.session['lid'], request.session['candidate_id'])
#         print(f"Emotion Detection Response: {response}")
#
#         # Determine response status
#         if response is None:
#             response = 0  # Default response for failure
#         else:
#             response = 1  # Ensure it returns 1 when emotions are detected
#
#         return JsonResponse({'status': response})  # Return JSON status
#     except Exception as e:
#         print(f"Error in play_newcam: {e}")  # Log exception
#         return JsonResponse({'status': 0})  # Default error response
#
# def handle_post(request, id):
#     if request.session.get("lg") != "lin":
#         return HttpResponse("<script>alert('Please login!');window.location='/'</script>")
#
#     request.session['count'] = int(request.session.get('count', 0)) + 1
#     selected_option = request.POST.get('answer')
#     correct_answer = request.POST.get('selected_answer')
#     print("selected_option",selected_option)
#     print("correct_answer",correct_answer)
#
#     if request.session.get('qcount') == request.session['count']:
#
#         mark = '1' if selected_option == correct_answer else '0'
#         print("markkkkkkkkkkk",mark)
#         import datetime
#         obj = test_result()
#         obj.STUDENT = user_tb.objects.get(LOGIN=request.session['lid'])
#         obj.mark = mark
#         obj.QUESTION_id = id
#         obj.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         obj.save()
#         print("objjjjjjjj", obj)
#         request.session['count'] = 0
#         request.session['qcount'] = 0
#         score = 0
#         data = test_result.objects.filter(USER=user_tb.objects.filter(LOGIN=request.session['lid']),
#                                             QUESTION__TEST_DETAILS=request.session['testid'])
#
#         for i in data:
#             score = score + int(i.mark)
#
#         candidatee = user_tb.objects.filter(LOGIN=request.session['lid'])
#
#         res1 = exam_tb.objects.filter(CANDIDATE=candidatee)
#         if res1.exists():
#             current_marks = res1[0].mark
#             a = str(int(current_marks) + int(mark))
#             request.session['mark'] = a
#             exam_tb.objects.filter(CANDIDATE=candidatee).update(mark=a)
#             cutoff = candidate_tb.objects.get(id=candidatee.id).VACCANCY.cutt_off
#             if int(a) > int(cutoff):
#                 candidate_tb.objects.filter(id=candidatee.id).update(status='scheduled')
#             else:
#                 candidate_tb.objects.filter(id=candidatee.id).update(status='examattended')
#
#         return render(request, 'user/view_test_result.html', {'score': score, "data": data})
#     else:
#         import datetime
#
#         mark = '1' if selected_option == correct_answer else '0'
#         print("mark",mark)
#
#         candidatee = user_tb.objects.get(LOGIN=request.session['lid'])
#         res1 = exam_tb.objects.filter(CANDIDATE__STUDENT__LOGIN=request.session['lid'])
#         print("res1",res1)
#         if res1.exists():
#             current_marks = res1[0].mark
#             a = str(int(current_marks) + int(mark))
#             request.session['mark'] = a
#             exam_tb.objects.filter(CANDIDATE=candidatee).update(mark=a)
#             cutoff = candidate_tb.objects.get(id=candidatee.id).VACCANCY.cutt_off
#             if int(a) > int(cutoff):
#                 candidate_tb.objects.filter(id=candidatee.id).update(status='scheduled')
#             else:
#                 candidate_tb.objects.filter(id=candidatee.id).update(status='examattended')
#
#         obj = test_result()
#         obj.USER = user_tb.objects.get(LOGIN=request.session['lid'])
#         obj.mark = mark
#         obj.QUESTION_id = id
#         obj.status = "exam attended"
#         obj.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         obj.save()
#         print("objjjjjjjj",obj)
#         candidate_tb.objects.filter(STUDENT__LOGIN=request.session['lid']).update(status="exam attended")
#
#         return redirect(f"/view_sample_question/{request.session['testid']}#aaa")
#
#
#
#
# def view_sample_question(request, id):
#
#     request.session['head'] = "VIEW SAMPLE QUESTION"
#
#     # data = user_tb.objects.filter(id=id)
#
#     # if data[0].no_of_unknown_person == 2 and data[0].multiple_person == 2:
#     #     return HttpResponse("<script>alert('Unauthorised events ocuured..Exam is blocked!!');window.location='/view_exam_date/'"+str(id)+"''</script>")
#     #
#
#     questions = question_tb.objects.filter(VACENCY=id)
#     print("len(questions)",questions)
#     # request.session['count'] = request.session['count']+1
#     print("request.session['count']",request.session['count'])
#
#
#     request.session['testid'] = id
#
#     if request.session['count'] < len(questions):
#         current_question = questions[request.session['count']]
#         print("current_question", current_question.question)
#     else:
#         return HttpResponse("<script>alert('No more questions available!');window.location='/view_shortlisted_list#aaa'</script>")
#
#     ar = {
#         'data': current_question,
#         'c': request.session['count']
#     }
#
#     return render(request, 'user/attend_exam.html', ar)
#
# #
# # def exam_details (request,id):
# #
# #     return render(request, "user/exam details.html", {"data": data})
#
#
#
# #
# # from django.http import JsonResponse
# # import cv2
# # from newcam import emotion  # Importing the function correctly
# #
# # def play_newcam(request):
# #     """
# #     Django view that captures a frame from the camera, detects emotion, and returns a JSON response.
# #     """
# #     try:
# #         # Capture frame from the camera
# #         cam = cv2.VideoCapture(0)
# #         ret, frame = cam.read()
# #         if not ret:
# #             print("Error: Could not capture frame from camera.")
# #             return JsonResponse({'status': 0})  # Return error if frame cannot be captured
# #
# #         # Call the emotion detection function and pass the frame
# #         # The emotion function now takes only the frame as input
# #         response = emotion(frame)
# #         # print(f"Emotion Detection Response: {response}")
# #
# #         obj = emotions()
# #         obj.emotions = response
# #         obj.CANDIDATE_id = user_tb.objects.get(LOGIN=request.session['lid']).id
# #         obj.save()
# #
# #              # Determine response status
# #         if response is None:
# #             response = 0  # Default response for failure (no face detected)
# #         else:
# #             response = 1  # Ensure it returns 1 when emotions are detected
# #
# #         return JsonResponse({'status': response})  # Return JSON status
# #
# #     except Exception as e:
# #         print(f"Error in play_newcam: {e}")  # Log exception
# #         return JsonResponse({'status': 0})  # Default error response



#====================================




#------- ATTEND EXAM --------

def applied_vacency(request):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head'] = "applied vacency"
    data=candidate_tb.objects.filter(USER__LOGIN=request.session['lid'],status='shortlisted')
    return render(request, "user/view applied vacency.html",{"data": data,"date":datetime.datetime.now().strftime("%Y-%m-%d"),'t':datetime.datetime.now().strftime("%H:%M")})



def view_shortlisted_list(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "VIEW SHORTLISTED LIST"

    data = candidate_tb.objects.filter(USER__LOGIN=request.session['lid'],status__in=['shortlisted','updated'])
    import datetime
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%H-%M")

    print("current_date",current_date)
    print("current_time",current_time)

    data1 = candidate_tb.objects.filter(interview_date=current_date,interview_time=current_time,USER__LOGIN=request.session['lid'])
    return render(request,"user/view_shortlisted_list.html",{"data":data,"data1":data1})


#--  exam attending --

def view_exam_date(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired');window.location='/'</script>")
    request.session['head'] = "VIEW EXAM DATE"
    request.session['candidate_id'] = id
    import datetime
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time_24 = datetime.datetime.now().strftime("%H:%M")
    current_time_12 = datetime.datetime.strptime(current_time_24, "%H:%M").strftime("%I:%M")

    print("current_dateeeeeeeeeee",current_date)
    print("current_time_12222222222",current_time_12)
    data = candidate_tb.objects.get(id=id)
    data1 = candidate_tb.objects.filter(exam_date=current_date, exam_time=current_time_12)
    request.session['count'] = 0
    return render(request,"user/view_exam_date.html",{"data":data,"data1":data1,"current_date":current_date})

#
# def submit_answer(request,id):
#
#
#     candidatee = candidate.objects.get(STUDENT__LOGIN=request.session['lid'])
#
#     question_index = int(request.POST.get('index'))
#     selected_answer = request.POST.get('selected_answer')
#
#     res = question.objects.filter(VACANCY=id).order_by('id')
#     if question_index < 0 or question_index >= len(res):
#         return HttpResponse("<script>alert('Invalid question index');window.location='/submit_answer#aaa'</script>")
#
#     single_question = res[question_index]
#
#     is_correct = (str(selected_answer) == str(single_question.answer))
#     print(selected_answer , single_question.answer,selected_answer == single_question.answer)
#     marks = 1 if is_correct else 0
#
#     res1=exam.objects.filter(CANDIDATE=candidatee)
#     if res1.exists():
#         current_marks = res1[0].mark
#         a = str(int(current_marks) + int(marks))
#         request.session['mark']=a
#         exam.objects.filter(CANDIDATE=candidatee).update(mark=a)
#         cutoff = candidate.objects.get(id=candidatee.id).VACANCY.cuttoff
#         if int(a) > int(cutoff):
#             candidate.objects.filter(id=candidatee.id).update(status='scheduled')
#         else:
#             candidate.objects.filter(id=candidatee.id).update(status='examattended')
#     else:
#         candidate_result=exam()
#         candidate_result.CANTIDATE=candidatee
#         candidate_result.mark=marks
#         candidate_result.save()
#
#     is_last_question = (question_index == len(res) - 1)
#
#     data = {
#         'status': "ok",
#         'is_last_question': is_last_question
#     }
#
#     return render(request, 'candidate/view_test_result.html', {'data': data})


def view_sample_question(request, id):

    request.session['head'] = "VIEW SAMPLE QUESTION"

    data = candidate_tb.objects.filter(id=id)

    # if data[0].no_of_unknown_person == 2 and data[0].multiple_person == 2:
    #     return HttpResponse("<script>alert('Unauthorised events ocuured..Exam is blocked!!');window.location='/view_exam_date/'"+str(id)+"''</script>")


    questions = question_tb.objects.filter(VACENCY=id)
    request.session['vid']=id
    print("len(questions)",questions)
    # request.session['count'] = request.session['count']+1
    print("request.session['count']",request.session['count'])


    request.session['testid'] = id

    if request.session['count'] < len(questions):
        current_question = questions[request.session['count']]
        print("current_question", current_question.question)
    else:
        return HttpResponse("<script>alert('No more questions available!');window.location='/view_shortlisted_list#aa'</script>")

    ar = {
        'data': current_question,
        'c': request.session['count']
    }

    return render(request, 'user/attend_exam.html', ar)

# def play_newcam(request):
#     from newcam import face_detection_and_emotion
#     # face_detection_and_emotion(request.session['lid'],request.session['candidate_id'])
#     response = face_detection_and_emotion(request.session['lid'], request.session['candidate_id'])
#     print("response",response)
#
#     return render(request, 'candidate/attend_exam.html',{'response': response})

from django.http import JsonResponse
import cv2
from newcam import emotion  # Importing the function correctly

def play_newcam(request):
    """
    Django view that captures a frame from the camera, detects emotion, and returns a JSON response.
    """
    try:
        # Capture frame from the camera
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if not ret:
            print("Error: Could not capture frame from camera.")
            return JsonResponse({'status': 0})  # Return error if frame cannot be captured
        cv2.imwrite( r"C:\Users\user\Downloads\real_time_mock_interview\real_time_mock_interview\mock_interview_app\static\a.jpg", frame)

        frame=cv2.imread(r"C:\Users\user\Downloads\real_time_mock_interview\real_time_mock_interview\mock_interview_app\static\a.jpg")
        # Call the emotion detection function and pass the frame
        # The emotion function now takes only the frame as input
        response = emotion(frame)
        # print(f"Emotion Detection Response: {response}")

        obj = emotions()
        obj.emotions = response
        obj.CANDIDATE_id = user_tb.objects.get(LOGIN=request.session['lid']).id
        obj.save()

             # Determine response status
        if response is None:
            response = 0  # Default response for failure (no face detected)
        else:
            response = 1  # Ensure it returns 1 when emotions are detected

        return JsonResponse({'status': response})  # Return JSON status

    except Exception as e:
        print(f"Error in play_newcam: {e}")  # Log exception
        return JsonResponse({'status': 0})  # Default error response











def handle_post(request, id):
    selected_option = request.POST.get('answer')  # User's selected answer
    correct_answer = request.POST.get('selected_answer')  # Correct answer for the question

    print("selected_option",selected_option)
    print("correct_answer",correct_answer)



    # Increment the question count
    request.session['count'] = int(request.session['count']) + 1

    # Ensure the selected_option and correct_answer are not None before proceeding
    if selected_option is None or correct_answer is None:
        return HttpResponse("Invalid input. Please try again.", status=400)

    # Mark calculation (1 for correct answer, 0 for incorrect)
    if selected_option == correct_answer:
        mark = 1
    else:
        mark = 0

    # Save the test result for this question
    import datetime
    try:
        obj = test_result()
        obj.USER = user_tb.objects.get(LOGIN=request.session['lid'])
        obj.mark = mark
        obj.QUESTION_id = id
        obj.status = 'exam attended'
        obj.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj.save()
    except Exception as e:
        # Log the error or send a notification
        print(f"Error saving test result: {e}")
        return HttpResponse("Error occurred while saving test results.", status=500)

    # If the test result has been saved successfully, we move on to update the exam table
    try:
        candidate_instance = candidate_tb.objects.get(USER__LOGIN=request.session['lid'], VACENCY_id=request.session['vid'])  # Correct candidate lookup

        # Initialize total_marks variable
        total_marks = mark  # If no existing record, the current mark will be the total for now

        # Check if the candidate already has an exam entry
        res1 = exam_tb.objects.filter(CANDIDATE=candidate_instance)

        if res1.exists():
            # Candidate exists, update the marks by adding the new mark
            current_marks = res1[0].mark
            total_marks = int(current_marks) + mark
            # Update the exam table with the new total_marks
            res1.update(mark=total_marks)  # Use update instead of filter and then update
        else:
            # Candidate doesn't have an entry in the exam table, create a new entry
            obj1 = exam_tb()
            obj1.mark = total_marks  # Set the initial mark if this is the first entry
            obj1.CANDIDATE_id = candidate_instance.id
            obj1.save()

        # Update the candidate status based on the total marks and cutoff
        cutoff = candidate_instance.VACENCY.cuttoff
        if total_marks > int(cutoff):
            candidate_tb.objects.filter(id=candidate_instance.id).update(status='scheduled')
        else:
            candidate_tb.objects.filter(id=candidate_instance.id).update(status='examattended')

        # Always set candidate status to "scheduled" after processing
        candidate_tb.objects.filter(USER__LOGIN=request.session['lid']).update(status="scheduled")

    except Exception as e:
        # Log the error or send a notification
        print(f"Error processing exam results: {e}")
        return HttpResponse("Error occurred while processing exam results.", status=500)

    # Return a redirect to the next sample question after successful processing
    return redirect(f"/view_sample_question/{request.session['testid']}#aa")





# ------- CHAT USER VS COMPANY


def chattt(request,u):
    if request.session['lid'] == '':
        return HttpResponse("<script>alert('Your session has expired');window.location='/';</script>")
    request.session['head']="CHAT"
    request.session['uid'] = u
    print("GGG  ", u)
    return render(request,'user/chat.html',{'u':u})


def chatsndd(request):
    d=datetime.datetime.now().strftime("%Y-%m-%d")
    # t=datetime.datetime.now().strftime("%H:%M:%S")
    c = request.session['lid']
    b=request.POST['n']
    print(b)
    m=request.POST['m']
    cc = user_tb.objects.get(LOGIN=request.session['lid'])
    print(c,"ccccccccccc")
    # cc=1
    uu = company_tb.objects.get(id=request.session['uid'])
    print(uu,"customer_id")
    print("cccccc",cc)
    print("uuuuuuuuuu",uu)
    obj=chat_tb()
    obj.date=d
    obj.type='user'
    obj.USER=cc
    obj.COMPANY=uu
    obj.chat=m
    obj.save()

    print(obj)
    v = {}
    if int(obj) > 0:
        v["status"] = "ok"
    else:
        v["status"] = "error"
    r = JsonResponse.encode(v)
    return r
# else:
#     return redirect('/')

def chatrplyy(request):
    # if request.session['log']=="lo":
    # c = request.session['lid']
    # rid=request.POST['rid']
    cc=user_tb.objects.get(LOGIN=request.session['lid'])

    # print("JJJJ  ",rid)
    uu=company_tb.objects.get(id=request.session['uid'])
    print("uuuuuuu",uu)
    res = chat_tb.objects.filter(USER=cc,COMPANY=uu)
    print(res)
    v = []
    if len(res) > 0:
        print(len(res))
        for i in res:
            v.append({
                'type':i.type,
                'chat':i.chat,
                'name': "user",

                # 'id':i.CUSTOMERS.id,
                # 'upic':i.USER.photo,
                'dtime':i.date,
                'tname':i.USER.name,
            })
        print(v)
        return JsonResponse({"status": "ok", "data": v})
    else:
        return JsonResponse({"status": "error"})
















