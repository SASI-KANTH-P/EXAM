from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.decorators import login_required
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your views here.


def baseRedirect(request):
    return redirect('accounts/register')

@login_required(login_url='accounts/login')
def dashboard(request):
    exam = Exam.objects.all()
    stu = Student.objects.all()
    registered = RegisteredExam.objects.all()
    print(registered)
    for regexam in registered:
        ru = str(request.user)
        regu = regexam.student.studentUser.username
        if regu == ru:
            return redirect('displaySelected')

    data = {
        'exam':exam,
        'stu': stu,
        'registered':registered
    }
    return render(request,'dashboard.html',data)


@login_required(login_url='accounts/login')
def registerExam(request):
    exam = Exam.objects.all()
    if request.method == 'POST':
        stu = Student.objects.order_by('name').get(name = request.POST['username'])
        for ex in exam:
            if request.POST.get(ex.examCode,False):
                regExam = RegisteredExam(student = stu,exam = ex)
                regExam.save()
        return redirect('displaySelected')
    return render(request,'four04.html')

def regAgain(request):
    exam = Exam.objects.all()
    stu = Student.objects.all()
    registered = RegisteredExam.objects.all()
    print(registered)
    excodes = []
    for regexam in registered:
        ru = str(request.user)
        regu = regexam.student.studentUser.username
        if regu == ru:
            excodes.append(regexam.exam.examCode)
            # return redirect('displaySelected')

    data = {
        'exam':exam,
        'excodes': excodes,
        'stu': stu,
        'registered':registered
    }
    return render(request,'alreadyreg.html',data)


@login_required(login_url='accounts/login')
def displaySelected(request):
    regExam = RegisteredExam.objects.all().distinct()
    data = {
        'regExam':regExam
    }
    return render(request,'display.html',data)




def some_view(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    textobj = p.beginText()
    textobj.setTextOrigin(inch,inch)
    textobj.setFont("Helvetica", 15)
    regExam = RegisteredExam.objects.all().distinct()
    ru = str(request.user)
    cost = 0
    count =0
    textobj.textLine("==========================================================")
    textobj.textLine("               Exam Registration Site")
    textobj.textLine("          Invoice  - Computer Generated")
    textobj.textLine("==========================================================")
    textobj.textLine(" ")
    textobj.textLine(" ")
    textobj.textLine(" ")
    for reg in regExam:
        if reg.student.studentUser.username == ru:
            count+=1
            textobj.textLine("{1} ) Exam Name : {0} ".format(reg.exam.examName,count))
            textobj.textLine("Exam Code : {0}".format(reg.exam.examCode))
            textobj.textLine("Exam Date : {0}".format(reg.exam.examDate))
            textobj.textLine(" ")
            textobj.textLine(" ")
            cost+=150
    textobj.textLine(" ")
    textobj.textLine("==========================================================")
    textobj.textLine("Total Fees  Rs.{0} ".format(cost))
    textobj.textLine("Bill Status : PAID")
    textobj.textLine("==========================================================")
    p.drawText(textobj)
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='{0}.pdf'.format(ru))

