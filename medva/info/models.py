import requests
from django import forms

from django.db import models
from info import utils
from django.contrib.auth.models import User as Baseuser
import datetime
from datetime import timedelta
import os


def create_path_event6(instance, filename):
    return os.path.join('catalog',
        filename
    )

def create_path_event8(instance, filename):
    return os.path.join('main',
        filename
    )


class Clinic(models.Model):
    clinic_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=216, null=True, default=None, blank=True)


class ClinicUser(models.Model):
    clinic_user_id = models.AutoField(primary_key=True)
    login = models.ForeignKey(Baseuser, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    post = models.CharField(max_length=216, null=True, default=None, blank=True)


class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=216, null=True, default=None, blank=True)


class ClinicDepartment(models.Model):
    clinic_department_id = models.AutoField(primary_key=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=216, null=True, default=None, blank=True)


class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=216, null=True, default=None, blank=True)
    id = models.IntegerField(default=0)

class DoctorDepartment(models.Model):
    doctor_department_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic_department = models.ForeignKey(ClinicDepartment, on_delete=models.CASCADE)


class Specialization(models.Model):
    specialization_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=216, null=True, default=None, blank=True)


class DoctorSpecialization(models.Model):
    doctor_specialization_id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=216, null=True, default=None, blank=True)
    sex = models.CharField(max_length=3, null=True, default=None, blank=True)
    id = models.IntegerField(default=0)
    birthdate = models.DateField(null=True, blank=True)


class ProtocolFileKit(models.Model):
    file_kit_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=216, null=True, default=None, blank=True)
    file = models.FileField(blank=True, default=None, upload_to=create_path_event6)
    whom = models.ForeignKey(Baseuser, on_delete=models.CASCADE)
    when = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    job = models.CharField(max_length=216, null=True, default=None, blank=True)


class Protocol(models.Model):
    protocol_id = models.AutoField(primary_key=True)
    consultation_date = models.DateField(null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic_department = models.ForeignKey(ClinicDepartment, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    file_kit = models.ForeignKey(ProtocolFileKit, on_delete=models.CASCADE)
    index1 = models.IntegerField(default=0)
    index2 = models.IntegerField(default=0)
    index3 = models.IntegerField(default=0)
    checked = models.BooleanField(default=False)
    has_justification = models.BooleanField(default=False)
    justification = models.FileField(blank=True, default=None, upload_to=create_path_event6)
    when = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Diagnosis(models.Model):
    diagnosis_id = models.AutoField(primary_key=True)
    mkb10 = models.CharField(max_length=10, null=True, default=None, blank=True)
    name = models.CharField(max_length=1024, null=True, default=None, blank=True)

    def __str__(self):
        return str(self.mkb10)


class ProtocolDiagnosis(models.Model):
    protocol_diagnosis_id = models.AutoField(primary_key=True)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=True)


class MedicalStandart(models.Model):
    medical_standart_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024, null=True, default=None, blank=True)
    urled = models.CharField(max_length=1024, null=True, default=None, blank=True)
    type = models.IntegerField(default=0)
    file = models.FileField(blank=True, default=None, upload_to=create_path_event6)


class MedicalStandartDiagnosis(models.Model):
    medical_standart_diagnosis_id = models.AutoField(primary_key=True)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    medical_standart = models.ForeignKey(MedicalStandart, on_delete=models.CASCADE)


class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    nmu_code = models.CharField(max_length=32)
    name_base = models.CharField(max_length=512, null=True, default=None, blank=True)
    versionnmu = models.CharField(max_length=32, null=True, default=None, blank=True)


class PrescriptionSynonym(models.Model):
    synonym_id = models.AutoField(primary_key=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    name = models.CharField(max_length=512, null=True, default=None, blank=True)
    extra1 = models.CharField(max_length=512, null=True, default=None, blank=True)
    extra2 = models.CharField(max_length=512, null=True, default=None, blank=True)
    extra3 = models.CharField(max_length=512, null=True, default=None, blank=True)
    extra4 = models.CharField(max_length=512, null=True, default=None, blank=True)
    extra5 = models.CharField(max_length=512, null=True, default=None, blank=True)
    based_on = models.CharField(max_length=216, null=True, default=None, blank=True)


class PrescriptionMedicalStandart(models.Model):
    prescription_medical_standart_id = models.AutoField(primary_key=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medical_standart = models.ForeignKey(MedicalStandart, on_delete=models.CASCADE)
    actuality = models.FloatField(default=0)


class ProtocolPrescriptionStandart(models.Model):
    protocol_prescription_standart_id = models.AutoField(primary_key=True)
    prescription_standart = models.ForeignKey(PrescriptionMedicalStandart, on_delete=models.CASCADE)
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    is_lacks = models.BooleanField(default=True)


class ProtocolPrescriptionReal(models.Model):
    protocol_prescription_real_id = models.AutoField(primary_key=True)
    real_text = models.CharField(max_length=512, null=True, default=None, blank=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)
    is_checked = models.BooleanField(default=False)
    has_justification = models.BooleanField(default=False)
    show_nmu = models.BooleanField(default=True)
    is_excess = models.BooleanField(default=True)


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=216, null=True, default=None, blank=True)
    date_list = models.CharField(max_length=216, null=True, default=None, blank=True)
    doctor_list = models.CharField(max_length=216, null=True, default=None, blank=True)
    spec_list = models.CharField(max_length=216, null=True, default=None, blank=True)
    depart_list = models.CharField(max_length=216, null=True, default=None, blank=True)
    index1_list = models.CharField(max_length=216, null=True, default=None, blank=True)
    index2_list = models.CharField(max_length=216, null=True, default=None, blank=True)
    when = models.DateField(auto_now_add=True, null=True, blank=True)
    clinic = models.ForeignKey(ClinicUser, on_delete=models.CASCADE)


class ReportProtocol(models.Model):
    report_protocol_id = models.AutoField(primary_key=True)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE)





