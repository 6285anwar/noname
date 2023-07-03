from django.shortcuts import render,redirect
from django.http import JsonResponse
import random
from django.contrib.auth import authenticate, login
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .models import *
from django.contrib.auth.models import User
import time




def landingpage(request):
    return render(request,'landing_page.html')


# ======================= >  ADMIN SECTION  <===========================#

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['Adm_id'] = user.id
            return redirect('admin_dashboard')
        else:
            return render(request,'Admin/admin_login.html')
    return render(request,'Admin/admin_login.html')


def admin_navbar(request):
    if 'Adm_id' in request.session:
        if request.session.has_key('Adm_id'):
                Adm_id = request.session['Adm_id']
        admin = User.objects.filter(id=Adm_id)
        return render(request,'Admin/admin_navbar.html',{'admin':admin}) 
    else:
        return redirect('/')


def admin_dashboard(request):
    if 'Adm_id' in request.session:
        if request.session.has_key('Adm_id'):
                Adm_id = request.session['Adm_id']
        admin = User.objects.filter(id=Adm_id)
        tutor = Tutor_Registration.objects.all()
        req_tutor = Tutor_Registration.objects.filter(status='0')

        tutor_count = Tutor_Registration.objects.all().count()
        tutor_active_count = Tutor_Registration.objects.filter(status='1').count()
        student_count = Student_Registration.objects.all().count()
        garde_count = Grades.objects.all().count()
        subject_count = Subjects.objects.all().count()


        return render(request,'Admin/admin_dashboard.html',{'admin':admin,'tutor':tutor,'req_tutor':req_tutor,'tutor_count':tutor_count,'tutor_active_count':tutor_active_count,'student_count':student_count,'garde_count':garde_count,'subject_count':subject_count}) 
    else:
        return redirect('/')

def admin_reg_accept(request,id):
    tutoraccept = Tutor_Registration.objects.get(id=id)
    tutoraccept.status = '1'
    formatted_id = str(id).zfill(3)
    tutorid = "TM" + formatted_id
    tutoraccept.tutor_id = tutorid


    sender_email = 'anwarsadik.disk1@gmail.com'
    receiver_email = tutoraccept.email
    password = 'ogxemcnlxvvbflhx'
    subject = 'Tutor Registration Accepted! Your Registration is Complete'
    message = 'Dear '+tutoraccept.fullname+','
    message += '\nWe are delighted to inform you that your tutor registration has been accepted! \n\nWelcome to our tutoring community. We appreciate your interest in joining our platform and sharing your knowledge and expertise with eager learners.'
    message += '\nYour registration is now complete, and we are excited to see you embark on this fulfilling journey of teaching and empowering students. As a registered tutor, you"ll have access to a wide range of resources and opportunities to connect with students seeking your guidance.\n'
    message += 'Here are the details of your tutor registration:\n'
    message += '\nTutor Name  : '+tutoraccept.fullname
    message += '\nUsername    : '+tutoraccept.username
    message += '\nPassword     : '+tutoraccept.password
    message += '\nTutor ID      : '+tutoraccept.tutor_id


    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print('Email sent successfully!')
        
    except Exception as e:
        print(f'An error occurred while sending the email: {str(e)}')
    finally:
        server.quit()

    tutoraccept.save()
    return redirect('admin_dashboard')


def admin_gradeandsub(request):
    if 'Adm_id' in request.session:
        if request.session.has_key('Adm_id'):
                Adm_id = request.session['Adm_id']
        admin = User.objects.filter(id=Adm_id)
        grade = Grades.objects.all()
        subs = Subjects.objects.all()

        for g in grade:
            tg=Tutor_Grades.objects.filter(grade=g).count()
            gs = Grades.objects.get(grade=g)
            gs.tutors_count=tg
            sg = Student_Registration.objects.filter(grade=g).count()
            gs.students_count=sg
            gs.save()
        return render(request,'Admin/admin_grades_sub.html',{'admin':admin,'grade':grade,'subs':subs}) 
    else:
        return redirect('/')




def admin_Addgrade(request):
    if request.method == 'POST':
        grade = request.POST['gr']
        g=Grades()
        g.grade=grade
        g.save()
        return redirect(admin_gradeandsub)

def admin_Addsubject(request):
    if request.method == 'POST':
        subs = request.POST['sub']
        g=Subjects()
        g.subject=subs
        g.save()
        return redirect(admin_gradeandsub)



def admin_students(request):
    if 'Adm_id' in request.session:
        if request.session.has_key('Adm_id'):
                Adm_id = request.session['Adm_id']
        admin = User.objects.filter(id=Adm_id)
        student = Student_Registration.objects.all()
        return render(request,'Admin/admin_student.html',{'admin':admin,'student':student}) 
    else:
        return redirect('/')


def admin_tutor_profileview(request,id):
    if 'Adm_id' in request.session:
        if request.session.has_key('Adm_id'):
                Adm_id = request.session['Adm_id']
        admin = User.objects.filter(id=Adm_id)
        t = Tutor_Registration.objects.get(id=id)
        return render(request,'Admin/admin_tutor_profileview.html',{'admin':admin,'t':t}) 
    else:
        return redirect('/')





def admin_tutor_reject(request,id):
    tutor = Tutor_Registration.objects.get(id=id)
    tutor.status = '-1'
    tutor.save()
    return redirect(admin_dashboard)




















# ======================= >  TUTOR SECTION  <===========================#

def tutor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if Tutor_Registration.objects.filter( username=username, password=password, status = '1').exists():
            tutor = Tutor_Registration.objects.get(username = request.POST['username'],password = request.POST['password'])
            request.session['Tutor_id'] = tutor.id
            return redirect('tutor_dashboard')
        else:
            return render(request,'Tutor/tutor_login.html',{'error':'INVALID CREDENTIALS'})
    else:

        return render(request,'Tutor/tutor_login.html')

def tutor_logout(request):
    if 'Tutor_id' in request.session:  
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/') 
    



def TutorSignUp(request):
    return render(request,'Tutor/tutor_signup.html')


def signup_ajax(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otpnumber = random.randint(1000, 9999)


        sender_email = 'anwarsadik.disk1@gmail.com'
        receiver_email = email
        password = 'ogxemcnlxvvbflhx'
        subject = 'TUTOR SIGNUP'
        message = 'Hi '
        message = 'TUTOR MARKETPLACE SIGNUP OTP.\n\n'
        message += 'OTP: ' + str(otpnumber)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print('Email sent successfully!')
        except Exception as e:
            print(f'An error occurred while sending the email: {str(e)}')
        finally:
            server.quit()


        response = {'otpnumber': otpnumber}
        return JsonResponse(response)











def email_authentication(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')

        t = Tutor_Registration()
        t.fullname = name
        t.email = email
        t.mobile = phone
        t.city = city
        t.save()
        print(t.id)
        response_data = {'id': t.id}
        return JsonResponse(response_data)

    response_data = {'message': 'Invalid AJAX request'}
    return JsonResponse(response_data, status=400)
    

def tutor_createprofile(request,id):
    tutor = Tutor_Registration.objects.filter(id=id)
    grades = Grades.objects.all()
    subs = Subjects.objects.all()
    return render(request,'Tutor/tutor_create_profile.html',{'tutor':tutor,'grades':grades,'subs':subs})


def username_checker(request):
    if request.method == 'POST':
        username = request.POST['value']
        if Tutor_Registration.objects.filter(username=username).exists():
            return JsonResponse({'exist':'exs'})
       


def tutor_profilesave(request,id):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        city = request.POST['city']
        gender = request.POST['gender']
        dob = request.POST['dob']
        adress = request.POST['adress']
        state = request.POST['state']
        contry = request.POST['contry']
        username = request.POST['username']
        password = request.POST['password']
        profile_picture = request.FILES.get('profile_pic', False)

        qualification = request.POST['qualification']
        qualification_cirt = request.FILES.get('qualification_pic', False)


        grade_1 = request.POST.getlist('grades[]')
        subject_1 = request.POST.getlist('subjects[]')


        t = Tutor_Registration.objects.get(id=id)
        t.name = name
        t.email = email
        t.phone = phone
        t.city = city
        t.gender = gender
        t.dateofbirth = dob
        t.address = adress
        t.state = state
        t.country = contry
        t.username = username
        t.password = password
        t.photo = profile_picture
        t.qualification = qualification
        t.qualification_cirt = qualification_cirt
        t.save()

        tg = Tutor_Registration.objects.get(id=t.id)
        for i in grade_1:
            Tutor_Grades.objects.create(tutor=tg,grade=i)
        for s in subject_1:
            Tutor_Subjects.objects.create(tutor=tg,subject=s)
        return redirect('tutor_login')



# def tutor_navbar(request):
#     if 'Tutor_id' in request.session:
#         if request.session.has_key('Tutor_id'):
#             Tutor_id = request.session['Tutor_id']
            
#         else:
#             return redirect('/')

#         tutor = Tutor_Registration.objects.filter(id=Tutor_id)

#         return render(request,'Tutor/tutor_navbar.html',{'tutor':tutor})
#     else:
#         return redirect('tutor_login')


def tutor_navbar(request):
    tutor_id = request.session.get('Tutor_id')
    if tutor_id:
        tutor_exists = Tutor_Registration.objects.filter(id=tutor_id, status=1).exists()
        if tutor_exists:
            tutor = Tutor_Registration.objects.filter(id=tutor_id)
            return render(request, 'Tutor/tutor_navbar.html', {'tutor': tutor})
    return redirect('tutor_login')

def tutor_dashboard(request):
    tutor_id = request.session.get('Tutor_id')
    if tutor_id:
        tutor_exists = Tutor_Registration.objects.filter(id=tutor_id, status=1).exists()
        if tutor_exists:
            tutor = Tutor_Registration.objects.filter(id=tutor_id)
            return render(request, 'Tutor/tutor_dashboard.html', {'tutor': tutor})
    
    return redirect('tutor_login')


def tutor_profile(request):
    tutor_id = request.session.get('Tutor_id')
    if tutor_id:
        tutor_exists = Tutor_Registration.objects.filter(id=tutor_id, status=1).exists()
        if tutor_exists:
            tutor = Tutor_Registration.objects.filter(id=tutor_id)
            return render(request, 'Tutor/tutor_profile.html', {'tutor': tutor})

    return redirect('tutor_login')





def tutor_time(request):
    tutor_id = request.session.get('Tutor_id')
    if tutor_id:
        tutor_exists = Tutor_Registration.objects.filter(id=tutor_id, status=1).exists()
        if tutor_exists:
            tutor = Tutor_Registration.objects.filter(id=tutor_id)

            tut = Tutor_Registration.objects.get(id=tutor_id)
            timeslots = tut.timeslots.all()

            timeslots_Mon = tut.timeslots.filter(day='Monday')
            timeslots_Tue = tut.timeslots.filter(day='Tuesday')
            timeslots_Wed = tut.timeslots.filter(day='Wednesday')
            timeslots_Thu = tut.timeslots.filter(day='Thursday')
            timeslots_Fri = tut.timeslots.filter(day='Friday')
            timeslots_Sat = tut.timeslots.filter(day='Saturday')
            timeslots_Sun = tut.timeslots.filter(day='Sunday')



            return render(request, 'Tutor/tutor_time.html', {'tutor': tutor,
                                                            'timeslots':timeslots,
                                                            'timeslots_Mon':timeslots_Mon,
                                                            'timeslots_Tue':timeslots_Tue,
                                                            'timeslots_Wed':timeslots_Wed,
                                                            'timeslots_Thu':timeslots_Thu,
                                                            'timeslots_Fri':timeslots_Fri,
                                                            'timeslots_Sat':timeslots_Sat,
                                                            'timeslots_Sun':timeslots_Sun
                                                        
                                                            })

    return redirect('tutor_login')


def save_times(request,id):
    if request.method == 'POST':
        days_of_week = {
            'Monday': (request.POST.getlist('Monday_from[]'), request.POST.getlist('Monday_to[]')),
            'Tuesday': (request.POST.getlist('Tuesday_from[]'), request.POST.getlist('Tuesday_to[]')),
            'Wednesday': (request.POST.getlist('Wednesday_from[]'), request.POST.getlist('Wednesday_to[]')),
            'Thursday': (request.POST.getlist('Thursday_from[]'), request.POST.getlist('Thursday_to[]')),
            'Friday': (request.POST.getlist('Friday_from[]'), request.POST.getlist('Friday_to[]')),
            'Saturday': (request.POST.getlist('Saturday_from[]'), request.POST.getlist('Saturday_to[]')),
            'Sunday': (request.POST.getlist('Sunday_from[]'), request.POST.getlist('Sunday_to[]'))
        }
        tutor = Tutor_Registration.objects.get(id=id)
        for day, (from_list, to_list) in days_of_week.items():
            for from_val, to_val in zip(from_list, to_list):
                if from_val and to_val:
                    print(f"{day} ===== From: {from_val}, To: {to_val}")

                    print(id)

                    timeslot = TimeSlot(day=day, from_time=from_val, to_time=to_val)
                    timeslot.save()
                    tutor.timeslots.add(timeslot)



        return redirect(tutor_time)
    return redirect(tutor_time)


def delete_save_time(request,id):
    print(id)

    timeslot = TimeSlot.objects.get(id=id)
    timeslot.delete()

    return redirect(tutor_time)




def tutor_price(request):
    tutor_id = request.session.get('Tutor_id')
    if tutor_id:
        tutor_exists = Tutor_Registration.objects.filter(id=tutor_id, status=1).exists()
        if tutor_exists:
            tutor = Tutor_Registration.objects.filter(id=tutor_id)
            return render(request, 'Tutor/tutor_price.html', {'tutor': tutor})
    return redirect('tutor_login')




def save_price(request,id):
    if request.method == 'POST':
        poh = request.POST['poh']
        pos = request.POST['pos']
        pgh = request.POST['pgh']
        pgs = request.POST['pgs']

        tutor = Tutor_Registration.objects.get(id=id)
        tutor.price_oneonone_hr = poh
        tutor.price_oneonone_session = pos
        tutor.price_group_hr = pgh
        tutor.price_group_session = pgs
        tutor.save()

    return redirect(tutor_price)


def tutor_gradeandsub(request):
    tutor_id = request.session.get('Tutor_id')
    if tutor_id:
        tutor_exists = Tutor_Registration.objects.filter(id=tutor_id, status=1).exists()
        if tutor_exists:
            tutor = Tutor_Registration.objects.filter(id=tutor_id)
            grades = Grades.objects.all()
            sub = Subjects.objects.all()
            tu_grade = Tutor_Grades.objects.filter(tutor=tutor_id)
            tu_sub = Tutor_Subjects.objects.filter(tutor=tutor_id)
            return render(request, 'Tutor/tutor_gradeandsub.html', {'tutor': tutor,'tu_grade':tu_grade,'grades':grades,'sub':sub,'tu_sub':tu_sub})
    return redirect('tutor_login')

def tutor_Gradechecker(request):
    tutor_id = request.session.get('Tutor_id')
    if tutor_id:
        tutor_exists = Tutor_Registration.objects.filter(id=tutor_id, status=1).exists()
        if tutor_exists:
            tutor = Tutor_Registration.objects.filter(id=tutor_id)
            tutor1 = Tutor_Registration.objects.get(id=tutor_id)

            if request.method == 'POST':
                grade = request.POST['value']
                if Tutor_Grades.objects.filter(tutor=tutor1).filter(grade=grade).exists():
                    print('hi')
                    return JsonResponse({'1':'1'})

                else:
                    return JsonResponse({'0':'0'})

    return redirect('tutor_login')

def tutor_Subchecker(request):
    tutor_id = request.session.get('Tutor_id')
    if tutor_id:
        tutor_exists = Tutor_Registration.objects.filter(id=tutor_id, status=1).exists()
        if tutor_exists:
            tutor = Tutor_Registration.objects.filter(id=tutor_id)
            tutor1 = Tutor_Registration.objects.get(id=tutor_id)

            if request.method == 'POST':
                grade = request.POST['value']
                print(grade)
                if Tutor_Subjects.objects.filter(tutor=tutor1).filter(subject=grade).exists():
                    print('hi')
                    return JsonResponse({'1':'1'})

                else:
                    return JsonResponse({'0':'0'})

    return redirect('tutor_login')




def tutor_addmore_grade(request):
    tutor_id = request.session.get('Tutor_id')
    if tutor_id:
        tutor_exists = Tutor_Registration.objects.filter(id=tutor_id, status=1).exists()
        if tutor_exists:
            tutor = Tutor_Registration.objects.filter(id=tutor_id)
            tutor1 = Tutor_Registration.objects.get(id=tutor_id)

            if request.method == 'POST':
                grade = request.POST['g']
                print(grade)
                t = Tutor_Grades()
                t.grade = grade
                t.tutor = tutor1
                t.save()
            return redirect('tutor_gradeandsub')
    return redirect('tutor_login')


def delete_tutorgrade(request,id):
    grd = Tutor_Grades.objects.get(id=id)
    grd.delete()
    return redirect('tutor_gradeandsub')
    

def tutor_addmore_sub(request):
    tutor_id = request.session.get('Tutor_id')
    if tutor_id:
        tutor_exists = Tutor_Registration.objects.filter(id=tutor_id, status=1).exists()
        if tutor_exists:
            tutor = Tutor_Registration.objects.filter(id=tutor_id)
            tutor1 = Tutor_Registration.objects.get(id=tutor_id)

            if request.method == 'POST':
                sub = request.POST['s']
                t = Tutor_Subjects()
                t.subject = sub
                t.tutor = tutor1
                t.save()
            return redirect('tutor_gradeandsub')
    return redirect('tutor_login')


def delete_tutorsub(request,id):
    grd = Tutor_Subjects.objects.get(id=id)
    grd.delete()
    return redirect('tutor_gradeandsub')
























































# ======================= >  STUDENT SECTION  <===========================#


def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if Student_Registration.objects.filter( username=username, password=password).exists():
            student = Student_Registration.objects.get(username = request.POST['username'],password = request.POST['password'])
            request.session['Std_id'] = student.id
            return redirect('student_dashboard')
        else:
            return render(request,'Student/student_login.html',{'error':'INVALID CREDENTIALS'})
    else:
        return render(request,'Student/student_login.html')


def student_logout(request):
    if 'Std_id' in request.session:  
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/') 

def student_signup(request):

    grades = Grades.objects.all()
    return render(request,'Student/student_signup.html',{'grades':grades})



def student_signup_ajax(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otpnumber = random.randint(1000, 9999)


        sender_email = 'anwarsadik.disk1@gmail.com'
        receiver_email = email
        password = 'ogxemcnlxvvbflhx'
        subject = 'Student SIGNUP'
        message = 'Hi '
        message = 'TUTOR MARKETPLACE STUDENT SIGNUP OTP.\n\n'
        message += 'OTP: ' + str(otpnumber)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print('Email sent successfully!')
        except Exception as e:
            print(f'An error occurred while sending the email: {str(e)}')
        finally:
            server.quit()


        response = {'otpnumber': otpnumber}
        return JsonResponse(response)
    



def student_email_authentication(request):
    if request.method == 'POST':
        studentName = request.POST.get('studentName')
        parentName = request.POST.get('parentName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        gradeis = request.POST.get('gradeis')


        s = Student_Registration()
        s.fullname = studentName
        s.parentfullname = parentName
        s.email = email
        s.mobile = phone
        s.city = city
        s.grade = gradeis
        s.save()
        print(s.id)
        response_data = {'id': s.id}
        return JsonResponse(response_data)

    response_data = {'message': 'Invalid AJAX request'}
    return JsonResponse(response_data, status=400)
    


def student_createprofile(request,id):
    student = Student_Registration.objects.filter(id=id)
    grades = Grades.objects.all()
    subs = Subjects.objects.all()
    return render(request,'Student/student_create_profile.html',{'student':student,'grades':grades,'subs':subs})



def student_profilesave(request,id):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        city = request.POST['city']
        gender = request.POST['gender']
        dob = request.POST['dob']
        adress = request.POST['adress']
        state = request.POST['state']
        contry = request.POST['contry']
        username = request.POST['username']
        password = request.POST['password']
        profile_picture = request.FILES.get('profile_pic', False)

        p_name = request.POST['pname']
        p_email = request.POST['pemail']
        p_phone = request.POST['pphone']
        p_city = request.POST['pcity']

        school = request.POST['institution']
        grade = request.POST['grade']



        s = Student_Registration.objects.get(id=id)
        s.name = name
        s.email = email
        s.phone = phone
        s.city = city
        s.gender = gender
        s.dateofbirth = dob
        s.address = adress
        s.state = state
        s.country = contry
        s.username = username
        s.password = password
        s.photo = profile_picture
        s.p_name = p_name
        s.p_email = p_email
        s.p_phone = p_phone
        s.p_city = p_city
        s.institution = school
        s.grade = grade
        s.save()

        return redirect('student_login')




def student_navbar(request):
    if 'Std_id' in request.session:
        if request.session.has_key('Std_id'):
            Std_id = request.session['Std_id']
        else:
            return redirect('/')
        std = Student_Registration.objects.filter(id=Std_id)
        return render(request,'Student/student_navbar.html',{'std':std})
    else:
        return redirect('tutor_login')

def student_dashboard(request):
    if 'Std_id' in request.session:
        if request.session.has_key('Std_id'):
            Std_id = request.session['Std_id']
        else:
            return redirect('/')

        std = Student_Registration.objects.filter(id=Std_id)
        return render(request,'Student/student_dashboard.html',{'std':std})
    else:
        return redirect('tutor_login')












