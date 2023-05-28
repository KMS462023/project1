from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [  
    # TODO: make webhook more secure
    path('', views.clinicboard, name="main"),
    path('clinicboard/<clinic_id>', views.clinicboard, name="clinicboard"),
    path('departmentboard/', views.departmentboard, name="departmentboardtotal"),
    path('departmentboard/<depart_id>', views.departmentboard, name="departmentboard"),
    path('departments/<clinic_id>', views.departments, name="departments"),
    path('doctors/<clinic_id>/<depart_id>', views.doctor, name="doctordep"),
    path('doctors/<clinic_id>/', views.doctor, name="doctors"),
    path('makekitprotocol/<clinic_id>/', views.makekitprotocol, name="makekitprotocolclinic"),
    path('makekitprotocol/', views.makekitprotocol, name="makekitprotocol"),
    path('showkitprotocol/<kit_id>', views.showkitprotocol, name="showkitprotocol"),
    path('archive/', views.archive, name="archive"),
    path('protocolview/<protocol_id>', views.protocolview, name="protocolview"),
    path('reportview/<report_id>', views.reportview, name="reportview"),
    path('protocollistview/<subject_type>/<subject_id>', views.protocollistview, name="protocollistview"),
    path('protocollistview/', views.protocollistview, name="protocollistviewtotal"),
    path('filterdep/', views.filterdep, name="filterdep"),
    path('filterdoc/', views.filterdoc, name="filterdoc"),
    path('filterspec/', views.filterspec, name="filterspec"),
    path('newreport/', views.newreport, name="newreport"),
    path('auth', views.auth, name="auth"),
]