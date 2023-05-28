import random
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render

from inmain.settings import DEBUG

from info.models import *

admin.site.register(Clinic)
admin.site.register(ClinicUser)
admin.site.register(ClinicDepartment)
admin.site.register(DoctorDepartment)
admin.site.register(Doctor)
admin.site.register(DoctorSpecialization)
admin.site.register(Department)
admin.site.register(Specialization)
admin.site.register(Patient)
admin.site.register(Protocol)
admin.site.register(ProtocolPrescriptionStandart)
admin.site.register(ProtocolFileKit)
admin.site.register(ProtocolDiagnosis)
admin.site.register(ProtocolPrescriptionReal)
admin.site.register(Diagnosis)
admin.site.register(MedicalStandartDiagnosis)
admin.site.register(MedicalStandart)
admin.site.register(Prescription)
admin.site.register(PrescriptionSynonym)
admin.site.register(PrescriptionMedicalStandart)
admin.site.register(Report)
admin.site.register(ReportProtocol)

