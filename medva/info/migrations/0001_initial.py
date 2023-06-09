# Generated by Django 3.2.6 on 2023-05-26 18:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import info.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('clinic_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default=None, max_length=216, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClinicDepartment',
            fields=[
                ('clinic_department_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default=None, max_length=216, null=True)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.clinic')),
            ],
        ),
        migrations.CreateModel(
            name='ClinicUser',
            fields=[
                ('clinic_user_id', models.AutoField(primary_key=True, serialize=False)),
                ('post', models.CharField(blank=True, default=None, max_length=216, null=True)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.clinic')),
                ('login', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default=None, max_length=216, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('diagnosis_id', models.AutoField(primary_key=True, serialize=False)),
                ('mkb10', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('name', models.CharField(blank=True, default=None, max_length=512, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('doctor_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default=None, max_length=216, null=True)),
                ('id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalStandart',
            fields=[
                ('medical_standart_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default=None, max_length=512, null=True)),
                ('urled', models.CharField(blank=True, default=None, max_length=216, null=True)),
                ('type', models.IntegerField(default=0)),
                ('file', models.FileField(blank=True, default=None, upload_to=info.models.create_path_event6)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('patient_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default=None, max_length=216, null=True)),
                ('sex', models.CharField(blank=True, default=None, max_length=3, null=True)),
                ('id', models.IntegerField(default=0)),
                ('birthdate', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('prescription_id', models.AutoField(primary_key=True, serialize=False)),
                ('nmu_code', models.CharField(max_length=32)),
                ('name_base', models.CharField(blank=True, default=None, max_length=512, null=True)),
                ('versionnmu', models.CharField(blank=True, default=None, max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PrescriptionMedicalStandart',
            fields=[
                ('prescription_medical_standart_id', models.AutoField(primary_key=True, serialize=False)),
                ('actuality', models.IntegerField(default=0)),
                ('medical_standart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.medicalstandart')),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.prescription')),
            ],
        ),
        migrations.CreateModel(
            name='Protocol',
            fields=[
                ('protocol_id', models.AutoField(primary_key=True, serialize=False)),
                ('consultation_date', models.DateField(blank=True, null=True)),
                ('index1', models.IntegerField(default=0)),
                ('index2', models.IntegerField(default=0)),
                ('index3', models.IntegerField(default=0)),
                ('checked', models.BooleanField(default=False)),
                ('has_justification', models.BooleanField(default=False)),
                ('justification', models.FileField(blank=True, default=None, upload_to=info.models.create_path_event6)),
                ('when', models.DateTimeField(auto_now_add=True, null=True)),
                ('clinic_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.clinicdepartment')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default=None, max_length=216, null=True)),
                ('date_list', models.CharField(blank=True, default=None, max_length=216, null=True)),
                ('doctor_list', models.CharField(blank=True, default=None, max_length=216, null=True)),
                ('spec_list', models.CharField(blank=True, default=None, max_length=216, null=True)),
                ('depart_list', models.CharField(blank=True, default=None, max_length=216, null=True)),
                ('index1_list', models.CharField(blank=True, default=None, max_length=216, null=True)),
                ('index2_list', models.CharField(blank=True, default=None, max_length=216, null=True)),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.clinicuser')),
            ],
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('specialization_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default=None, max_length=216, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReportProtocol',
            fields=[
                ('report_protocol_id', models.AutoField(primary_key=True, serialize=False)),
                ('protocol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.protocol')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.report')),
            ],
        ),
        migrations.CreateModel(
            name='ProtocolPrescriptionStandart',
            fields=[
                ('protocol_prescription_standart_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_lacks', models.BooleanField(default=True)),
                ('prescription_standart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.prescriptionmedicalstandart')),
                ('protocol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.protocol')),
            ],
        ),
        migrations.CreateModel(
            name='ProtocolPrescriptionReal',
            fields=[
                ('protocol_prescription_real_id', models.AutoField(primary_key=True, serialize=False)),
                ('real_text', models.CharField(blank=True, default=None, max_length=512, null=True)),
                ('is_checked', models.BooleanField(default=False)),
                ('has_justification', models.BooleanField(default=False)),
                ('is_excess', models.BooleanField(default=True)),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.prescription')),
                ('protocol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.protocol')),
            ],
        ),
        migrations.CreateModel(
            name='ProtocolFileKit',
            fields=[
                ('file_kit_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default=None, max_length=216, null=True)),
                ('file', models.FileField(blank=True, default=None, upload_to=info.models.create_path_event6)),
                ('when', models.DateTimeField(auto_now_add=True, null=True)),
                ('job', models.CharField(blank=True, default=None, max_length=216, null=True)),
                ('whom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProtocolDiagnosis',
            fields=[
                ('protocol_diagnosis_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_main', models.BooleanField(default=True)),
                ('diagnosis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.diagnosis')),
                ('protocol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.protocol')),
            ],
        ),
        migrations.AddField(
            model_name='protocol',
            name='file_kit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.protocolfilekit'),
        ),
        migrations.AddField(
            model_name='protocol',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.patient'),
        ),
        migrations.AddField(
            model_name='protocol',
            name='specialization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.specialization'),
        ),
        migrations.CreateModel(
            name='PrescriptionSynonym',
            fields=[
                ('synonym_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default=None, max_length=512, null=True)),
                ('extra1', models.CharField(blank=True, default=None, max_length=512, null=True)),
                ('extra2', models.CharField(blank=True, default=None, max_length=512, null=True)),
                ('extra3', models.CharField(blank=True, default=None, max_length=512, null=True)),
                ('extra4', models.CharField(blank=True, default=None, max_length=512, null=True)),
                ('extra5', models.CharField(blank=True, default=None, max_length=512, null=True)),
                ('based_on', models.CharField(blank=True, default=None, max_length=216, null=True)),
                ('prescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.prescription')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalStandartDiagnosis',
            fields=[
                ('medical_standart_diagnosis_id', models.AutoField(primary_key=True, serialize=False)),
                ('diagnosis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.diagnosis')),
                ('medical_standart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.medicalstandart')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorSpecialization',
            fields=[
                ('doctor_specialization_id', models.AutoField(primary_key=True, serialize=False)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.doctor')),
                ('specialization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.specialization')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorDepartment',
            fields=[
                ('doctor_department_id', models.AutoField(primary_key=True, serialize=False)),
                ('clinic_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.clinicdepartment')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.doctor')),
            ],
        ),
        migrations.AddField(
            model_name='clinicdepartment',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.department'),
        ),
    ]
