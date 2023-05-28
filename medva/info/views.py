import logging
from django.views import View
from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from django.utils import timezone
from django.forms import modelformset_factory
from django.contrib.auth.models import User as Baseuser
from info.models import *
from django.utils.crypto import get_random_string
from inmain.storage_backends import MediaStorage
from collections import OrderedDict
import random
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import pymorphy2
import itertools
import redis
import json
from django.http import HttpResponse
import datetime
from django.core.paginator import Paginator
from datetime import time
from django.db.models import Max
from datetime import timedelta
from string import digits as diglist
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
# from PIL import Image
from django.core.mail import send_mail
import base64
from django.db.models import F
from random import randrange
import pickle
from inmain.settings import DEBUG
from django.db.models import Avg, Count, Min, Sum
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from django.core.mail import EmailMessage

from celery import shared_task, current_task
from celery.result import AsyncResult
from info.tasks import do_work, do_work2






def circlemake(protocols):
    total = protocols['lack'] + protocols['excess'] + protocols['normal']
    circleparam = [
        [int((protocols['lack'] / total) * 100), int(100 - int((protocols['lack'] / total) * 100)), 25],
        [int((protocols['excess'] / total) * 100), int(100 - int((protocols['excess'] / total) * 100)), 25 + (100-int((protocols['lack'] / total) * 100))],
        [int((protocols['normal'] / total) * 100), int(100 - int((protocols['normal'] / total) * 100)), 25 + (100-int((protocols['lack'] / total) * 100) - int((protocols['excess'] / total) * 100))],
        [protocols['lack'], protocols['excess'], protocols['normal'], total]

    ]
    return circleparam


def divide_list(input_list):
    divided_list = []
    for i in range(0, len(input_list), 4):
        sublist = input_list[i:i+4]
        divided_list.append(sublist)
    return divided_list

logger = logging.getLogger(__name__)

@login_required(login_url='/auth')
def clinicboard(request, clinic_id=None):
    user0 = request.user

    if user0.is_authenticated:
        a = 'redkmsvd!leaders46moscow'
        methodist = ClinicUser.objects.filter(login=user0).order_by('clinic__name')

        if clinic_id:
            if ClinicUser.objects.get(clinic__clinic_id=clinic_id) in methodist:
                pass

        cliniclist = []
        for userclinic in methodist:
            clinic = userclinic.clinic


            totalprotocols = Protocol.objects.filter(clinic_department__clinic=clinic)
            lackandover = totalprotocols.aggregate(lack=Sum('index1'),
                                                   excess=Sum('index2'),
                                                   normal=Sum('index3')
                                                   )
            # lack = ProtocolPrescriptionStandart.objects.filter(protocol__in=totalprotocols, is_lacks=True).count()
            # over = ProtocolPrescriptionReal.objects.filter(protocol__in=totalprotocols, is_excess=True).count()
            dayprottemp = totalprotocols.filter(consultation_date__gt=datetime.datetime.today().date() - timedelta(days=1)).aggregate(lack=Sum('index1'),
                                                                                                                         excess=Sum('index2'),
                                                                                                                         normal=Sum('index3')
                                                                                                                       )
            if dayprottemp['lack']:
                dayprot = circlemake(dayprottemp)
            else:
                dayprot = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0, 0]
    ]
            weekprottemp = totalprotocols.filter(consultation_date__gt=datetime.datetime.today().date() - timedelta(weeks=1)).aggregate(lack=Sum('index1'),
                                                                                                                         excess=Sum('index2'),
                                                                                                                         normal=Sum('index3')
                                                                                                                         )
            if weekprottemp['lack']:
                weekprot = circlemake(weekprottemp)
            else:
                weekprot = [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0, 0]
                ]
            monthprottemp = totalprotocols.filter(consultation_date__gt=datetime.datetime.today().date() - timedelta(days=31)).aggregate(lack=Sum('index1'),
                                                                                                                         excess=Sum('index2'),
                                                                                                                         normal=Sum('index3')
                                                                                                                         )
            if monthprottemp['lack']:
                monthprot = circlemake(monthprottemp)
            else:
                monthprot = [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0, 0]
                ]
            yearprottemp = totalprotocols.filter(consultation_date__gt=datetime.datetime.today().date() - timedelta(days=365)).aggregate(lack=Sum('index1'),
                                                                                                                         excess=Sum('index2'),
                                                                                                                         normal=Sum('index3')
                                                                                                                         )
            if yearprottemp['lack']:
                yearprot = circlemake(yearprottemp)
            else:
                yearprot = [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0, 0]
                ]
            cliniclist.append([clinic, lackandover, dayprot, weekprot, monthprot, yearprot, ['d', 'w', 'm', 'y']])

        context = {"cliniclist": cliniclist,}
        return render(request, 'web/main-page.html', context)


def departmentboard(request, depart_id=None):
    user0 = request.user

    if user0.is_authenticated:
        is_sliding = False
        methodist = ClinicDepartment.objects.filter(clinic__clinicuser__login=user0).order_by('name')
        if depart_id:
            if ClinicDepartment.objects.get(clinic_department_id=depart_id) in methodist:
                is_sliding = True
                print('ss')
        startdep = 0
        slidecnt = 0

        cliniclist = []

        for depart in methodist:
            slidecnt+=1
            # depart = userclinic.department
            if is_sliding:
                if int(depart_id) == depart.clinic_department_id:
                    startdep = slidecnt - 1
                    print('find')
                print(startdep)
            totalprotocols = Protocol.objects.filter(clinic_department=depart)
            lackandover = totalprotocols.aggregate(lack=Sum('index1'),
                                                   excess=Sum('index2'),
                                                   normal=Sum('index3')
                                                   )
            # lack = ProtocolPrescriptionStandart.objects.filter(protocol__in=totalprotocols, is_lacks=True).count()
            # over = ProtocolPrescriptionReal.objects.filter(protocol__in=totalprotocols, is_excess=True).count()
            dayprottemp = totalprotocols.filter(
                consultation_date__gt=datetime.datetime.today().date() - timedelta(days=1)).aggregate(
                lack=Sum('index1'),
                excess=Sum('index2'),
                normal=Sum('index3')
                )
            if dayprottemp['lack']:
                dayprot = circlemake(dayprottemp)
            else:
                dayprot = [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0, 0]
                ]
            weekprottemp = totalprotocols.filter(
                consultation_date__gt=datetime.datetime.today().date() - timedelta(weeks=1)).aggregate(
                lack=Sum('index1'),
                excess=Sum('index2'),
                normal=Sum('index3')
                )
            if weekprottemp['lack']:
                weekprot = circlemake(weekprottemp)
            else:
                weekprot = [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0, 0]
                ]
            monthprottemp = totalprotocols.filter(
                consultation_date__gt=datetime.datetime.today().date() - timedelta(days=31)).aggregate(
                lack=Sum('index1'),
                excess=Sum('index2'),
                normal=Sum('index3')
                )
            if monthprottemp['lack']:
                monthprot = circlemake(monthprottemp)
            else:
                monthprot = [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0, 0]
                ]
            yearprottemp = totalprotocols.filter(
                consultation_date__gt=datetime.datetime.today().date() - timedelta(days=365)).aggregate(
                lack=Sum('index1'),
                excess=Sum('index2'),
                normal=Sum('index3')
                )
            if yearprottemp['lack']:
                yearprot = circlemake(yearprottemp)
            else:
                yearprot = [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0, 0]
                ]
            cliniclist.append([depart, lackandover, dayprot, weekprot, monthprot, yearprot, ['d', 'w', 'm', 'y']])

        context={'cliniclist':cliniclist, 'startdep':startdep}
        return render(request, 'web/depart-board.html', context)


def departments(request, clinic_id=None):
    user0 = request.user

    if user0.is_authenticated:
        if clinic_id:
            if ClinicUser.objects.filter(clinic__clinic_id=clinic_id, login=user0).exists():
                pass
        if request.GET.get('search'):
            search = request.GET.get('search')
            departments = ClinicDepartment.objects.filter(clinic__clinic_id=clinic_id, department__name__icontains=search).order_by('department__name')
        else:
            departments = ClinicDepartment.objects.filter(clinic__clinic_id=clinic_id).order_by('department__name')

        cliniclist = []
        for depart in departments:
            # depart = userclinic.department

            totalprotocols = Protocol.objects.filter(clinic_department=depart)
            lackandover = totalprotocols.aggregate(lack=Sum('index1'),
                                                   excess=Sum('index2'),
                                                   normal=Sum('index3')
                                                   )
            # lack = ProtocolPrescriptionStandart.objects.filter(protocol__in=totalprotocols, is_lacks=True).count()
            # over = ProtocolPrescriptionReal.objects.filter(protocol__in=totalprotocols, is_excess=True).count()
            if totalprotocols:
                lackandovercircle = circlemake(lackandover)
            else:
                lackandovercircle = [
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0, 0]
                ]
            totalamount = totalprotocols.count()
            doctors = DoctorDepartment.objects.filter(clinic_department=depart).count()
            cliniclist.append([depart, lackandovercircle, totalamount, doctors])

        paginator = Paginator(cliniclist, 6)
        paging = False
        if request.GET.get("page"):
            paging = True
            page_number = request.GET.get("page")
        else:
            page_number = 1
        cliniclist = paginator.get_page(page_number)

        context = {"cliniclist": cliniclist, }
        return render(request, 'web/departments-list.html', context)


def doctor(request, clinic_id, depart_id=None):
    user0 = request.user

    if user0.is_authenticated:
        if clinic_id:
            if ClinicUser.objects.filter(clinic__clinic_id=clinic_id, login=user0).exists():
                pass

        if depart_id:
            departments = ClinicDepartment.objects.filter(clinic__clinic_id=clinic_id, department_id=depart_id)
        else:
            departments = ClinicDepartment.objects.filter(clinic__clinic_id=clinic_id).order_by('department__name')

        cliniclist = []

        if request.GET.get('search'):
            search = request.GET.get('search')
            doctors = Doctor.objects.filter(doctordepartment__clinic_department__in=departments, name__icontains=search)
        else:
            doctors = Doctor.objects.filter(doctordepartment__clinic_department__in=departments)

        for doctor in doctors:
            specialization = ""
            for spec in Specialization.objects.filter(doctorspecialization__doctor=doctor):
                if not specialization:
                    specialization+= spec.name
                else:
                    specialization += (", " + spec.name)
            department = ""
            for depart in Department.objects.filter(clinicdepartment__doctordepartment__doctor=doctor):
                if not department:
                    department += depart.name
                else:
                    department += (", " + depart.name)
            lastprotocol = Protocol.objects.filter(doctor=doctor).last()
            cliniclist.append([doctor, specialization, department, lastprotocol])

        paginator = Paginator(cliniclist, 6)
        paging = False
        if request.GET.get("page"):
            paging = True
            page_number = request.GET.get("page")
        else:
            page_number = 1
        cliniclist = paginator.get_page(page_number)

        context = {"cliniclist": cliniclist, }
        return render(request, 'web/doctors-page.html', context)


def newreport(request):
    user0 = request.user

    if user0.is_authenticated:

        methodist = ClinicDepartment.objects.filter(clinic__clinicuser__login=user0).first()



        clinic = methodist.clinic

        totalprotocols = Protocol.objects.filter(clinic_department__clinic=clinic)

        departsearch = ''
        doctorsearch = ''
        specsearch = ''
        if request.GET.get('lack'):
            lacksearch = request.GET.get('lack')
        else:
            lacksearch = 'false'
        if request.GET.get('excess'):
            excesssearch = request.GET.get('excess')
        else:
            excesssearch = 'false'



        if request.GET.get('searchcat2') or request.GET.get('doctor'):
            if not request.GET.get('doctor') == request.GET.get('searchcat2'):
                if request.GET.get('doctor'):
                    if not (request.GET.get('searchcat2') in request.GET.get('doctor')):
                        special = request.GET.get('doctor') + ";" + request.GET.get('searchcat2')
                    else:
                        special = request.GET.get('doctor').replace(request.GET.get('searchcat2') + ';',
                                                                    '').replace(request.GET.get('searchcat2'), '')
                else:
                    special = request.GET.get('searchcat2')
                doctorsearch = special
                specials = []
                print(1)
                for dep in Doctor.objects.filter(doctordepartment__clinic_department__clinic=clinic):
                    if dep.name.lower() in special.split(';'):
                        # for spec in special.split(';'):
                        specials.append(dep)
                print(specials)
                totalprotocols = totalprotocols.filter(doctor__in=specials)
            else:
                doctorsearch = ''
        if request.GET.get('searchcat1') or request.GET.get('depart'):
            if not request.GET.get('depart')==request.GET.get('searchcat1'):
                if request.GET.get('depart'):
                    if not (request.GET.get('searchcat1') in request.GET.get('depart')):
                        special = request.GET.get('depart')+";"+request.GET.get('searchcat1')
                    else:
                        special = request.GET.get('depart').replace(request.GET.get('searchcat1')+';','').replace(request.GET.get('searchcat1'),'')
                else:
                    special = request.GET.get('searchcat1')
                departsearch = special
                specials = []
                print(1)
                for dep in Department.objects.filter(clinicdepartment__clinic=clinic):
                    if dep.name.lower() in special.split(';'):
                # for spec in special.split(';'):
                        specials.append(dep)
                print(specials)
                totalprotocols = totalprotocols.filter(clinic_department__department__in=specials)
            else:
                doctorsearch=''
        if request.GET.get('searchcat3') or request.GET.get('spec'):
            if not request.GET.get('spec') == request.GET.get('searchcat3'):
                if request.GET.get('spec'):
                    if not (request.GET.get('searchcat3') in request.GET.get('spec')):
                        special = request.GET.get('spec') + ";" + request.GET.get('searchcat3')
                    else:
                        special = request.GET.get('spec').replace(request.GET.get('searchcat3') + ';',
                                                                    '').replace(request.GET.get('searchcat3'), '')
                else:
                    special = request.GET.get('searchcat3')
                specsearch = special
                specials = []
                print(1)
                for dep in Specialization.objects.filter(protocol__clinic_department__clinic=clinic):
                    if dep.name.lower() in special.split(';'):
                        # for spec in special.split(';'):
                        specials.append(dep)
                print(specials)
                totalprotocols = totalprotocols.filter(specialization__in=specials)
            else:
                specsearch = ''
        if request.GET.get('prot_date'):
            prot_date = request.GET.get('prot_date')
            prot_dates = []
            for prot in prot_date.split('-'):
                dat1 = prot.split('.')
                prot_dates.append(datetime.date(year=dat1[2], month=dat1[1], day=dat1[0]))
            totalprotocols.filter(when__gt=prot_dates[0], when__lt=prot_dates[1])
        if request.GET.get('lackchange') == 'true':
            if request.GET.get('lack') == 'false':
                totalprotocols = totalprotocols.filter(index1__gt=0)
                lacksearch = 'true'
            else:
                lacksearch = 'false'
        if request.GET.get('excesschange') == 'true':
            if request.GET.get('excess') == 'false':
                totalprotocols = totalprotocols.filter(index2__gt=0)
                excesssearch = 'true'
            else:
                excesssearch = 'false'
        if request.GET.get('creqtereport') == 'create':
            if request.GET.get('reportname'):
                naming = request.GET.get('reportname')
            else:
                naming = 'Отчет'
            newreport = Report(name=naming, clinic=ClinicUser.objects.filter(login=user0).first())
            newreport.doctor_list=request.GET.get('doctor')
            newreport.spec_list=request.GET.get('spec')
            newreport.depart_list=request.GET.get('depart')
            newreport.index1_list=request.GET.get('excess')
            newreport.index2_list=request.GET.get('lack')
            newreport.save()
            for protocol in totalprotocols:
                newreportprotocol = ReportProtocol(report=newreport, protocol=protocol)
                newreportprotocol.save()
            return redirect('archive')

        context = {'departsearch': departsearch, 'doctorsearch': doctorsearch,
                   'specsearch':specsearch, 'excesssearch': excesssearch, 'lacksearch': lacksearch}
        return render(request, 'web/report-page.html', context)


# def newkitprotocol(request, clinic_id=None):
#     user0 = request.user
#
#     if user0.is_authenticated:
#
#         methodist = ClinicUser.objects.filter(login=user0, clinic_id=clinic_id).order_by('clinic__name')
#
#         if clinic_id:
#             if ClinicUser.objects.get(clinic__clinic_id=clinic_id) in methodist:
#                 clinic = ClinicUser.objects.get(clinic__clinic_id=clinic_id)
#             else:
#                 clinic = None
#         else:
#             clinic = ClinicUser.objects.filter(clinic__clinic_id=clinic_id).first()
#
#         # if request.method == "POST":
#         #     if request.FILES.get('kit'):
#         #
#         return render(request, 'web/protocols-page.html')


def makekitprotocol(request, clinic_id=None):
    user0 = request.user

    if user0.is_authenticated:

        methodist = ClinicUser.objects.filter(login=user0, clinic_id=clinic_id).order_by('clinic__name')

        if clinic_id:
            if ClinicUser.objects.get(clinic__clinic_id=clinic_id) in methodist:
                clinic = ClinicUser.objects.get(clinic__clinic_id=clinic_id).clinic
            else:
                clinic = None
        else:
            clinic = ClinicUser.objects.filter(login=user0).first().clinic


        if request.method == "POST":
            if request.FILES.get('kit'):
                file = request.FILES.get('kit')

                newkit = ProtocolFileKit(name=file.name, file=file, whom=user0)
                newkit.save()
                job = do_work2.delay([clinic, newkit.file_kit_id])
                newkit.job=job.id
                newkit.job='123321'
                newkit.save()
                return redirect('showkitprotocol', newkit.file_kit_id)
            else:
                return redirect('makekitprotocol')
        return render(request, 'web/protocols-page.html')


def poll_state(request):
    """ A view to report the progress to the user """
    if 'job' in request.GET:
        job_id = request.GET['job']
    else:
        return JsonResponse({'job': 'none'})

    job = AsyncResult(job_id)
    data = job.state
    return HttpResponse(json.dumps(data), mimetype='application/json')


def showkitprotocol(request, kit_id):
    user0 = request.user

    if user0.is_authenticated:

        if ProtocolFileKit.objects.filter(whom=user0, file_kit_id=kit_id).exists():
            kitjob = ProtocolFileKit.objects.get(file_kit_id=kit_id)

            context = {'kitjob': kitjob}
            return render(request, 'web/protocols-done-page.html', context)


def archive(request):
    user0 = request.user

    if user0.is_authenticated:

        reportlist = Report.objects.filter(clinic__login=user0).order_by('-when')

        reports = []
        for report in reportlist:
            specials = ''
            docts = ''
            departs = ''
            if report.depart_list:
                depart = report.depart_list
                for dep in depart.split(','):
                    # totalprotocols.filter(clinic_department__clinic_department_id=departs)
                    departs+= (dep + ', ')
                report.depart_list = depart
            if report.doctor_list:
                doct = report.doctor_list

                for doc in doct.split(','):
                    docts += (doc + ', ')
            if report.spec_list:
                special = report.spec_list
                for spec in special.split(','):
                    specials+= (spec + ', ')
            reports.append([report, specials, docts, departs])

        paginator = Paginator(reports, 4)
        paging = False
        if request.GET.get("page"):
            paging = True
            page_number = request.GET.get("page")
        else:
            page_number = 1
        reports = paginator.get_page(page_number)
        context = {'reports': reports}
        return render(request, 'web/archive-page.html', context)


def protocolview(request, protocol_id):
    user0 = request.user

    if user0.is_authenticated:

        methodist = ClinicDepartment.objects.filter(clinic__clinicuser__login=user0)

        protocollisttemp = []
        if Protocol.objects.filter(clinic_department__in=methodist, protocol_id=protocol_id).exists():
            protocol=Protocol.objects.get(clinic_department__in=methodist, protocol_id=protocol_id)
            if ProtocolPrescriptionReal.objects.filter(protocol=protocol).exists():
                diagnosis = ProtocolDiagnosis.objects.filter(protocol=protocol)
                prescriptionstandart = PrescriptionMedicalStandart.objects.filter(protocolprescriptionstandart__protocol=protocol)
                stnes = prescriptionstandart.filter(actuality=1)
                stextra = prescriptionstandart.filter(actuality__lt=1)
                lack = prescriptionstandart.filter(protocolprescriptionstandart__is_lacks=True)
                prescriptionreal = ProtocolPrescriptionReal.objects.filter(protocol=protocol)
                excess = prescriptionreal.filter(is_excess=True, is_checked=False)
                normal = prescriptionreal.filter(is_excess=False)
                lackcount = lack.count()
                excesscount = excess.count()
                normcount = prescriptionreal.count() - excesscount

                protocols = {'lack': lackcount, 'excess': excesscount, 'normal': normcount}
                total = protocols['lack'] + protocols['excess'] + protocols['normal']
                circleparam = [
                    [int((protocols['lack'] / total) * 100), int(100 - int((protocols['lack'] / total) * 100)), 25],
                    [int((protocols['excess'] / total) * 100), int(100 - int((protocols['excess'] / total) * 100)),
                     25 + (100 - int((protocols['lack'] / total) * 100))],
                    [int((protocols['normal'] / total) * 100), int(100 - int((protocols['normal'] / total) * 100)),
                     25 + (100 - int((protocols['lack'] / total) * 100) - int((protocols['excess'] / total) * 100))],
                    [protocols['lack'], protocols['excess'], protocols['normal'], total]

                ]


                analyzelist = []
                startex = True
                for presp in excess:
                    if startex:
                        analyzelist.append(['01', presp])
                        startex = False
                    else:
                        analyzelist.append(['1', presp])

                startla = True
                for presp in lack:
                    if startla:
                        analyzelist.append(['02', presp])
                        startla = False
                    else:
                        analyzelist.append(['2', presp])

                startnorm = True
                for presp in normal:
                    if startnorm:
                        analyzelist.append(['03', presp])
                        startnorm = False
                    else:
                        analyzelist.append(['3', presp])



                divided_list_analyze = []
                for i in range(0, len(analyzelist), 4):
                    sublist = analyzelist[i:i + 4]
                    divided_list_analyze.append(sublist)

                standartlist = []
                startstandartneed = True
                startstandartextra = True
                for presp in prescriptionstandart.order_by('-actuality'):
                    if not presp.actuality < 1.0:
                        if startstandartneed:
                            standartlist.append(['01', presp])
                            startstandartneed = False
                        else:
                            standartlist.append(['1', presp])
                    else:
                        if startstandartextra:
                            standartlist.append(['02', presp])
                            startstandartextra = False
                        else:
                            standartlist.append(['2', presp])

                divided_list_standart = []
                for i in range(0, len(standartlist), 4):
                    sublist = standartlist[i:i + 4]
                    divided_list_standart.append(sublist)



                divided_list_real = []
                for i in range(0, len(prescriptionreal), 5):
                    sublist = prescriptionreal[i:i + 5]
                    divided_list_real.append(sublist)

                if request.method == "POST":
                    if request.POST.get('actiontype'):
                        if request.FILES.get('reasons'):
                            protocol.justification = request.FILES.get('reasons')
                            protocol.has_justification = True
                            protocol.save()
                        action = request.POST.get('actiontype')
                        if action == 'cancel':
                            for prot in prescriptionreal:
                                if request.POST.get('confirm' + str(prot.protocol_prescription_real_id)):
                                    prot.is_checked = False
                                    prot.save()
                        elif action == 'confirm':
                            for prot in prescriptionreal:
                                if request.POST.get('confirm' + str(prot.protocol_prescription_real_id)):
                                    prot.is_checked = True
                                    prot.save()
                # context = [protocol, diagnosis, prescriptionstandart, stnes, stextra, lack, prescriptionreal, excess,lackcount, excesscount, normcount]
                context = {'protocol': protocol, 'diagnosis': diagnosis,
                           'divided_list': divided_list_analyze, 'divided_list_standart': divided_list_standart,
                           'divided_list_real': divided_list_real, 'circleparam': circleparam}
                return render(request, 'web/protocols-inside-page.html', context)



def reportview(request, report_id):
    user0 = request.user

    if user0.is_authenticated:

        methodist = ClinicDepartment.objects.filter(clinic__clinicuser__login=user0)

        if Report.objects.filter(clinic__login=user0, report_id=report_id).exists():
            report = Report.objects.get(report_id=report_id)
            totalprotocols = Protocol.objects.filter(reportprotocol__report=report)

            clinic = report.clinic.clinic
            departments = ClinicDepartment.objects.filter(clinic=clinic).order_by('department__name')
            doctors = Doctor.objects.filter(doctordepartment__clinic_department__clinic=clinic).order_by('name')
            specialiazations = Specialization.objects.filter(doctorspecialization__doctor__in=doctors)


            departsearch = ''
            doctorsearch = ''
            specsearch = ''
            if request.GET.get('lack'):
                lacksearch = request.GET.get('lack')
            else:
                lacksearch = 'false'
            if request.GET.get('excess'):
                excesssearch = request.GET.get('excess')
            else:
                excesssearch = 'false'



            if request.GET.get('searchcat2') or request.GET.get('doctor'):
                if not request.GET.get('doctor') == request.GET.get('searchcat2'):
                    if request.GET.get('doctor'):
                        if not (request.GET.get('searchcat2') in request.GET.get('doctor')):
                            special = request.GET.get('doctor') + ";" + request.GET.get('searchcat2')
                        else:
                            special = request.GET.get('doctor').replace(request.GET.get('searchcat2') + ';',
                                                                        '').replace(request.GET.get('searchcat2'), '')
                    else:
                        special = request.GET.get('searchcat2')
                    doctorsearch = special
                    specials = []
                    print(1)
                    for dep in Doctor.objects.filter(doctordepartment__clinic_department__clinic=clinic):
                        if dep.name.lower() in special.split(';'):
                            # for spec in special.split(';'):
                            specials.append(dep)
                    print(specials)
                    totalprotocols = totalprotocols.filter(doctor__in=specials)
                else:
                    doctorsearch = ''
            if request.GET.get('searchcat1') or request.GET.get('depart'):
                if not request.GET.get('depart')==request.GET.get('searchcat1'):
                    if request.GET.get('depart'):
                        if not (request.GET.get('searchcat1') in request.GET.get('depart')):
                            special = request.GET.get('depart')+";"+request.GET.get('searchcat1')
                        else:
                            special = request.GET.get('depart').replace(request.GET.get('searchcat1')+';','').replace(request.GET.get('searchcat1'),'')
                    else:
                        special = request.GET.get('searchcat1')
                    departsearch = special
                    specials = []
                    print(1)
                    for dep in Department.objects.filter(clinicdepartment__clinic=clinic):
                        if dep.name.lower() in special.split(';'):
                    # for spec in special.split(';'):
                            specials.append(dep)
                    print(specials)
                    totalprotocols = totalprotocols.filter(clinic_department__department__in=specials)
                else:
                    doctorsearch=''
            if request.GET.get('searchcat3') or request.GET.get('spec'):
                if not request.GET.get('spec') == request.GET.get('searchcat3'):
                    if request.GET.get('spec'):
                        if not (request.GET.get('searchcat3') in request.GET.get('spec')):
                            special = request.GET.get('spec') + ";" + request.GET.get('searchcat3')
                        else:
                            special = request.GET.get('spec').replace(request.GET.get('searchcat3') + ';',
                                                                        '').replace(request.GET.get('searchcat3'), '')
                    else:
                        special = request.GET.get('searchcat3')
                    specsearch = special
                    specials = []
                    print(1)
                    for dep in Specialization.objects.filter(protocol__clinic_department__clinic=clinic):
                        if dep.name.lower() in special.split(';'):
                            # for spec in special.split(';'):
                            specials.append(dep)
                    print(specials)
                    totalprotocols = totalprotocols.filter(specialization__in=specials)
                else:
                    specsearch = ''
            if request.GET.get('prot_date'):
                prot_date = request.GET.get('prot_date')
                prot_dates = []
                for prot in prot_date.split('-'):
                    dat1 = prot.split('.')
                    prot_dates.append(datetime.date(year=dat1[2], month=dat1[1], day=dat1[0]))
                totalprotocols.filter(when__gt=prot_dates[0], when__lt=prot_dates[1])
            if request.GET.get('lackchange') == 'true':
                if request.GET.get('lack') == 'false':
                    totalprotocols = totalprotocols.filter(index1__gt=0)
                    lacksearch = 'true'
                else:
                    lacksearch = 'false'
            if request.GET.get('excesschange') == 'true':
                if request.GET.get('excess') == 'false':
                    totalprotocols = totalprotocols.filter(index2__gt=0)
                    excesssearch = 'true'
                else:
                    excesssearch = 'false'
            if request.GET.get('creqtereport') == 'create':
                newreport = Report(name='Отчет', clinic=ClinicUser.objects.filter(login=user0).first())
                newreport.doctor_list=request.GET.get('doctor')
                newreport.spec_list=request.GET.get('spec')
                newreport.depart_list=request.GET.get('depart')
                newreport.index1_list=request.GET.get('excess')
                newreport.index2_list=request.GET.get('lack')
                newreport.save()
                for protocol in totalprotocols:
                    newreportprotocol = ReportProtocol(report=newreport, protocol=protocol)
                    newreportprotocol.save()
                return redirect('archive')
            protocol_list = []
            for protocol in totalprotocols:
                diagnosis = ProtocolDiagnosis.objects.get(protocol=protocol, is_main=True)

                protocol_list.append(
                    [protocol, diagnosis])

            paginator = Paginator(protocol_list, 7)
            paging = False
            if request.GET.get("page"):
                paging = True
                page_number = request.GET.get("page")
            else:
                page_number = 1
            protocol_list = paginator.get_page(page_number)
            print(departsearch)
            context = {'protocol_list': protocol_list, 'departsearch': departsearch, 'doctorsearch': doctorsearch,
                       'specsearch':specsearch, 'excesssearch': excesssearch, 'lacksearch': lacksearch}
            return render(request, 'web/report-page2.html', context)



def protocollistview(request, subject_type=None, subject_id=None):
    user0 = request.user

    if user0.is_authenticated:

        methodist = ClinicDepartment.objects.filter(clinic__clinicuser__login=user0)

        if methodist.exists():

            if subject_type == 'clinic':
                if ClinicUser.objects.filter(login=user0, clinic__clinic_id=subject_id).exists():
                    clinic = Clinic.objects.get(clinic_id=subject_id)
                    totalprotocols = Protocol.objects.filter(clinic_department__clinic=clinic)
                else:
                    clinic = None
                    totalprotocols = []
            elif subject_type == 'department':
                if ClinicDepartment.objects.filter(clinic__clinicuser__login=user0, clinic_department_id=subject_id).exists():
                    clinic = ClinicDepartment.objects.get(clinic_department_id=subject_id).clinic
                    totalprotocols = Protocol.objects.filter(clinic_department_id=subject_id)
                else:
                    clinic = None
                    totalprotocols = []
            elif subject_type == 'doctor':
                if DoctorDepartment.objects.filter(clinic_department__in=methodist, doctor__doctor_id=subject_id).exists():
                    clinic = DoctorDepartment.objects.filter(doctor__doctor_id=subject_id).first().clinic_department.clinic
                    totalprotocols = Protocol.objects.filter(doctor_id=subject_id, clinic_department__clinic=clinic)
                else:
                    clinic=None
                    totalprotocols = []
            else:
                clinic = methodist.first().clinic
                totalprotocols = Protocol.objects.filter(clinic_department__clinic=clinic)

            departments = ClinicDepartment.objects.filter(clinic=clinic).order_by('department__name')
            doctors = Doctor.objects.filter(doctordepartment__clinic_department__clinic=clinic).order_by('name')
            specialiazations = Specialization.objects.filter(doctorspecialization__doctor__in=doctors)
            departsearch = ''
            doctorsearch = ''
            specsearch = ''
            if request.GET.get('lack'):
                lacksearch = request.GET.get('lack')
            else:
                lacksearch = 'false'
            if request.GET.get('excess'):
                excesssearch = request.GET.get('excess')
            else:
                excesssearch = 'false'



            if request.GET.get('searchcat2') or request.GET.get('doctor'):
                if not request.GET.get('doctor') == request.GET.get('searchcat2'):
                    if request.GET.get('doctor'):
                        if not (request.GET.get('searchcat2') in request.GET.get('doctor')):
                            special = request.GET.get('doctor') + ";" + request.GET.get('searchcat2')
                        else:
                            special = request.GET.get('doctor').replace(request.GET.get('searchcat2') + ';',
                                                                        '').replace(request.GET.get('searchcat2'), '')
                    else:
                        special = request.GET.get('searchcat2')
                    doctorsearch = special
                    specials = []
                    print(1)
                    for dep in Doctor.objects.filter(doctordepartment__clinic_department__clinic=clinic):
                        if dep.name.lower() in special.split(';'):
                            # for spec in special.split(';'):
                            specials.append(dep)
                    print(specials)
                    totalprotocols = totalprotocols.filter(doctor__in=specials)
                else:
                    doctorsearch = ''
            if request.GET.get('searchcat1') or request.GET.get('depart'):
                if not request.GET.get('depart')==request.GET.get('searchcat1'):
                    if request.GET.get('depart'):
                        if not (request.GET.get('searchcat1') in request.GET.get('depart')):
                            special = request.GET.get('depart')+";"+request.GET.get('searchcat1')
                        else:
                            special = request.GET.get('depart').replace(request.GET.get('searchcat1')+';','').replace(request.GET.get('searchcat1'),'')
                    else:
                        special = request.GET.get('searchcat1')
                    departsearch = special
                    specials = []
                    print(1)
                    for dep in Department.objects.filter(clinicdepartment__clinic=clinic):
                        if dep.name.lower() in special.split(';'):
                    # for spec in special.split(';'):
                            specials.append(dep)
                    print(specials)
                    totalprotocols = totalprotocols.filter(clinic_department__department__in=specials)
                else:
                    doctorsearch=''
            if request.GET.get('searchcat3') or request.GET.get('spec'):
                if not request.GET.get('spec') == request.GET.get('searchcat3'):
                    if request.GET.get('spec'):
                        if not (request.GET.get('searchcat3') in request.GET.get('spec')):
                            special = request.GET.get('spec') + ";" + request.GET.get('searchcat3')
                        else:
                            special = request.GET.get('spec').replace(request.GET.get('searchcat3') + ';',
                                                                        '').replace(request.GET.get('searchcat3'), '')
                    else:
                        special = request.GET.get('searchcat3')
                    specsearch = special
                    specials = []
                    print(1)
                    for dep in Specialization.objects.filter(protocol__clinic_department__clinic=clinic):
                        if dep.name.lower() in special.split(';'):
                            # for spec in special.split(';'):
                            specials.append(dep)
                    print(specials)
                    totalprotocols = totalprotocols.filter(specialization__in=specials)
                else:
                    specsearch = ''
            if request.GET.get('prot_date'):
                prot_date = request.GET.get('prot_date')
                prot_dates = []
                for prot in prot_date.split('-'):
                    dat1 = prot.split('.')
                    prot_dates.append(datetime.date(year=dat1[2], month=dat1[1], day=dat1[0]))
                totalprotocols.filter(when__gt=prot_dates[0], when__lt=prot_dates[1])
            if request.GET.get('lackchange') == 'true':
                if request.GET.get('lack') == 'false':
                    totalprotocols = totalprotocols.filter(index1__gt=0)
                    lacksearch = 'true'
                else:
                    lacksearch = 'false'
            if request.GET.get('excesschange') == 'true':
                if request.GET.get('excess') == 'false':
                    totalprotocols = totalprotocols.filter(index2__gt=0)
                    excesssearch = 'true'
                else:
                    excesssearch = 'false'
            if request.GET.get('creqtereport') == 'create':
                newreport = Report(name='Отчет', clinic=ClinicUser.objects.filter(login=user0).first())
                newreport.doctor_list=request.GET.get('doctor')
                newreport.spec_list=request.GET.get('spec')
                newreport.depart_list=request.GET.get('depart')
                newreport.index1_list=request.GET.get('excess')
                newreport.index2_list=request.GET.get('lack')
                newreport.save()
                for protocol in totalprotocols:
                    newreportprotocol = ReportProtocol(report=newreport, protocol=protocol)
                    newreportprotocol.save()
                return redirect('archive')
            protocol_list = []
            for protocol in totalprotocols:
                diagnosis = ProtocolDiagnosis.objects.get(protocol=protocol, is_main=True)

                protocol_list.append(
                    [protocol, diagnosis])

            paginator = Paginator(protocol_list, 7)
            paging = False
            if request.GET.get("page"):
                paging = True
                page_number = request.GET.get("page")
            else:
                page_number = 1
            protocol_list = paginator.get_page(page_number)
            print(departsearch)
            context = {'protocol_list': protocol_list, 'departsearch': departsearch, 'doctorsearch': doctorsearch,
                       'specsearch':specsearch, 'excesssearch': excesssearch, 'lacksearch': lacksearch}
            return render(request, 'web/record-page.html', context)



def filterdep(request):
    if request.POST.get('action') == 'filter':
        received_data1 = request.POST.get('product')
        user0 = request.user

        if user0.is_authenticated:
            sent_data_aft2 = []
            departaments = Department.objects.filter(clinicdepartment__clinic__clinic_id=request.POST.get('clinic')).values_list('name', flat=True)

            for dep in departaments:
                if received_data1 in dep.lower():
                    sent_data_aft2.append([dep.lower()])
            response_data = {}
            response_data['data'] = str(sent_data_aft2).replace("'", '"')
            return JsonResponse(response_data)


def filterdoc(request):
    if request.POST.get('action') == 'filter':
        received_data1 = request.POST.get('product')
        user0 = request.user

        if user0.is_authenticated:
            sent_data_aft2 = []
            departaments = Doctor.objects.filter(doctordepartment__clinic_department__clinic=request.POST.get('clinic')).values_list('name', flat=True)

            for dep in departaments:
                if received_data1 in dep.lower():
                    sent_data_aft2.append([dep.lower()])
            response_data = {}
            response_data['data'] = str(sent_data_aft2).replace("'", '"')
            return JsonResponse(response_data)


def filterspec(request):
    if request.POST.get('action') == 'filter':
        received_data1 = request.POST.get('product')
        user0 = request.user

        if user0.is_authenticated:
            sent_data_aft2 = []
            departaments = Specialization.objects.filter(protocol__clinic_department__clinic=request.POST.get('clinic')).values_list('name', flat=True)

            for dep in departaments:
                if received_data1 in dep.lower():
                    sent_data_aft2.append([dep.lower()])
            response_data = {}
            response_data['data'] = str(sent_data_aft2).replace("'", '"')
            return JsonResponse(response_data)



def auth(request):
    if request.method == "POST":
        username = request.POST['name']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("main")
            else:
                pass
        else:
            pass
        user = None
        context = {"user": user}
        return render(request, 'web/login-page.html', context)
    else:
        user = None
        context = {"user":
                       user}
        return render(request, 'web/login-page.html', context)


def uploadmkb():
    # Загружаем список из файла
    with open('need_data_4.pkl', 'rb') as f:
        need_data_4 = pickle.load(f)
        for key in need_data_4:
            newmkb = Diagnosis(mkb10=key, name=need_data_4[key])
            newmkb.save()


def uploadnmu():
    # Загружаем список из файла
    with open('need_data_3.pkl', 'rb') as f:
        need_data_3 = pickle.load(f)
        for key in need_data_3:
            if not Prescription.objects.filter(nmu_code=key).exists():
                newnmu = Prescription(nmu_code=key, name_base=need_data_3[key], versionnmu='2020')
                newnmu.save()


def uploadstandart():
    # Загружаем список из файла
    with open('need_data_5.pkl', 'rb') as f:
        need_data_5 = pickle.load(f)
        for key in need_data_5:
            if Diagnosis.objects.filter(mkb10=key).exists():
                diag = Diagnosis.objects.get(mkb10=key)
                for doc in need_data_5[key]:
                    if not MedicalStandartDiagnosis.objects.filter(diagnosis__mkb10=key, medical_standart__name=doc[1]).exists():
                        if not MedicalStandart.objects.filter(name=doc[1]).exists():
                            newdoc = MedicalStandart(name=doc[1], urled=doc[0], type=1)
                            newdoc.save()
                        else:
                            newdoc = MedicalStandart.objects.get(name=doc[1])
                        newdiagstandart = MedicalStandartDiagnosis(diagnosis=diag, medical_standart=newdoc)
                        newdiagstandart.save()


def uploadstandartprescription():
    # Загружаем список из файла
    with open('need_data_1.pkl', 'rb') as f:
        need_data_1 = pickle.load(f)
        for key in need_data_1:
            if Diagnosis.objects.filter(mkb10=key).exists():
                diag = Diagnosis.objects.get(mkb10=key)
                if MedicalStandartDiagnosis.objects.filter(diagnosis=diag, medical_standart__type=1).exists():
                    standarts = MedicalStandartDiagnosis.objects.filter(diagnosis=diag, medical_standart__type=1)
                    for medstandart in standarts:
                        standart = medstandart.medical_standart
                        for nmu in need_data_1[key]:
                            if Prescription.objects.filter(nmu_code=nmu[0]).exists():
                                prescript = Prescription.objects.get(nmu_code=nmu[0])
                                if not PrescriptionMedicalStandart.objects.filter(prescription=prescript, medical_standart=standart).exists():
                                    newpresctiptstandart = PrescriptionMedicalStandart(medical_standart=standart, prescription=prescript, actuality=float(nmu[2].replace(',','.')))
                                    newpresctiptstandart.save()


def semanticmapupdate():
    r = redis.StrictRedis(
        host="",
        port=6380,
        password="",
        ssl=True,
        ssl_ca_certs='YandexInternalRootCA.crt'
    )

    with open('reversed_index_idf.pkl', 'rb') as f:
        reversed_index_idf = pickle.load(f)
        cnt = 0
        for key in reversed_index_idf:

            # Define your object
            a = reversed_index_idf[key]

            # Serialize the object to JSON
            serialized_a = json.dumps(a)
            r.set(key, serialized_a)
            cnt+=1
            print(cnt)
