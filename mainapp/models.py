from django.db import models



class TimeSlot(models.Model):
    day = models.CharField(max_length=20)
    from_time = models.TimeField()
    to_time = models.TimeField()

class Tutor_Registration(models.Model):
    tutor_id = models.CharField(max_length=240,null=True,default='')
    fullname = models.CharField(max_length=240, null=True)
    email = models.EmailField(max_length=240, null=True)
    address = models.CharField(max_length=240, null=True)
    mobile = models.CharField(max_length=240, null=True)

    gender = models.CharField(max_length=240, null=True)
    dateofbirth = models.CharField(max_length=240, null=True)
    city = models.CharField(max_length=240, null=True)
    state = models.CharField(max_length=240, null=True)
    country = models.CharField(max_length=240, null=True)
    username = models.CharField(max_length=240, null=True)
    password = models.CharField(max_length=240, null=True)
    photo = models.FileField(upload_to='images/', null=True, blank=True)
    qualification = models.CharField(max_length=150, null=True)
    qualification_cirt = models.FileField(upload_to='images/', null=True, blank=True)

    otp = models.CharField(max_length=4,default='0000')

    status = models.CharField(max_length=4, null=True, default='0')


    timeslots = models.ManyToManyField(TimeSlot)

    price_oneonone_hr = models.CharField(max_length=10,default='0')
    price_oneonone_session = models.CharField(max_length=10,default='0')

    price_group_hr = models.CharField(max_length=10,default='0')
    price_group_session = models.CharField(max_length=10,default='0')







    def __str__(self):
        return self.fullname











class Grades(models.Model):
    grade = models.CharField(max_length=240, null=True)
    tutors_count = models.CharField(max_length=240, null=True)
    students_count = models.CharField(max_length=240, null=True)

    def __str__(self):
        return self.grade

class Subjects(models.Model):
    subject = models.CharField(max_length=240, null=True)
    def __str__(self):
        return self.subject

class Tutor_Grades(models.Model):
    tutor = models.ForeignKey(Tutor_Registration, on_delete=models.CASCADE,null=True, blank=True)
    grade = models.CharField(max_length=240, null=True)
    def __str__(self):
        return self.tutor.fullname

class Tutor_Subjects(models.Model):
    tutor = models.ForeignKey(Tutor_Registration, on_delete=models.CASCADE,null=True, blank=True)
    subject = models.CharField(max_length=240, null=True)
    def __str__(self):
        return self.tutor.fullname

class Student_Registration(models.Model):
    fullname = models.CharField(max_length=240, null=True)
    parentfullname = models.CharField(max_length=240, null=True)
    email = models.EmailField(max_length=240, null=True)
    city = models.CharField(max_length=240, null=True)
    mobile = models.CharField(max_length=240, null=True)

    gender = models.CharField(max_length=240, null=True)
    dateofbirth = models.CharField(max_length=240, null=True)
    address = models.CharField(max_length=240, null=True)
    state = models.CharField(max_length=240, null=True)
    country = models.CharField(max_length=240, null=True)
    username = models.CharField(max_length=240, null=True)
    password = models.CharField(max_length=240, null=True)
    photo = models.FileField(upload_to='images/', null=True, blank=True)


    p_name = models.CharField(max_length=240, null=True)
    p_email = models.CharField(max_length=240, null=True)
    p_phone = models.CharField(max_length=240, null=True)
    p_city = models.CharField(max_length=240, null=True)

    institution = models.CharField(max_length=240, null=True)
    grade = models.CharField(max_length=240, null=True)


    



    def __str__(self):
        return self.fullname
