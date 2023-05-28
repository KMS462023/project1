from django import template
import itertools
from inmain.settings import *
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
register = template.Library()
# from easy_select2.widgets import Select2, Select2Multiple
import datetime
import os

@register.filter
def filename(value):
    return os.path.basename(value.file.name)


@register.simple_tag
def val(obj):
    val=[]
    for att in obj.__getstate__():
        attval = getattr(obj, att)
        val.append(attval)
    val=val[1:]
        # val.append((att, getattr(obj,att)))
        # val.append(att)
    return val


@register.simple_tag
def checkpdf(obj):
    if obj:
        if obj.name.lower().endswith(('.pdf',)):
            return True
        else:
            return False
    else:
        return False


@register.simple_tag
def obnames(obj):
    val=[]
    for att in obj.__getstate__():
        val.append(att)
    val=val[1:]
        # val.append((att, getattr(obj,att)))
        # val.append(att)
    return val


class CycleNode(template.Node):
    def __init__(self, cyclevars):
        self.cycle_iter = iter(cyclevars)

    def __str__(self):
        return next(self.cycle_iter)

    def render(self, context):
        return next(self.cycle_iter)


@register.simple_tag
def mycycle(obj):
    return (next(obj))

@register.simple_tag
def mycycle2(obj):
    next(obj)
    return ""

@register.simple_tag
def myc(cyclevars):
    return (iter(cyclevars))

@register.simple_tag
def checkr(obj):
    if obj[0] == "True":
        return True
    if obj[0] == "False":
        return False

@register.simple_tag
def chen(obj, name):
    a1 = getattr(obj, str(name))
    if a1:
        return a1
    else:
        return ""

@register.simple_tag
def listing(obj, num):
    a1 = obj[int(num)]
    return a1

@register.simple_tag
def getcon(obj, num):
    a1 = obj[num]
    return a1

@register.simple_tag
def multich(obj):
    if obj is not None:
        if obj.startswith("['") and obj.endswith("']"):
            a1 = obj.strip('[]')
            a2 = a1.strip("'")
            a3 = a2.replace("', '", ";  ")
            return a3
        else:
            return obj
    else:
        return None

@register.simple_tag
def itr1(obj):
    b = obj.__iter__()
    return b

@register.simple_tag
def ch1(obj):
    if obj == "True":
        return True
    else:
        return False

@register.simple_tag
def summa(obj):
    sum = "input-text##" + obj + '##' + 'text'
    return sum

@register.simple_tag
def urldo(obj):
    sum = "https://system.forinform.ru/observe/" + obj
    return sum

@register.simple_tag
def featurelist(obj):
    sum = obj.split(';')
    return sum


@register.simple_tag
def datenorm(obj):
    sum = obj.strftime("%Y-%m-%d")
    return sum

@register.filter(name='clearurl1')
def clearurl1(value):
    newval = value.replace("@", "")
    newval = newval.replace(" ", "")
    return newval


@register.filter(name='shortdesc')
def shortdesc(value):
    if len(value) > 30:
        newval = value[:30]+'...'
    else:
        newval = value
    return newval





@register.filter(name='format_date_archive')
def format_date_archive(value):
    return value.strftime("%d.%m")


@register.filter(name='clearurl2')
def clearurl2(value):
    newval = value.replace("@", "")
    newval = newval.replace(" ", "")
    newval = newval.replace("https://", "")
    newval = newval.replace("facebook.com/", "")
    newval = newval.replace("www.", "")
    # newval = newval.replace("profile.php?id=", "")
    return newval


@register.filter(name='clearurl3')
def clearurl3(value):
    newval = value.replace("@", "")
    newval = newval.replace(" ", "")
    newval = newval.replace("https://", "")
    newval = newval.replace("vk.com/", "")
    newval = newval.replace("www.", "")
    return newval



@register.filter(name='addclass')
def addclass(value, arg):
    arg_list = arg.split('##')
    return value.as_widget(attrs={'class': arg_list[0], 'placeholder': arg_list[1], 'type': arg_list[2]})

@register.filter(name='addclass2')
def addclass2(value, arg):
    arg_list = arg.split('##')
    return value.as_widget(attrs={'class': arg_list[0], 'placeholder': arg_list[1], 'type': arg_list[2]},
                           widget=forms.widgets.DateTimeInput(attrs={'type': 'date', }))

@register.filter(name='addclass3')
def addclass3(value, arg):
    arg_list = arg.split('##')
    return value.as_widget(attrs={'class': arg_list[0], 'placeholder': arg_list[1], 'type': arg_list[2]},
                           widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}, format=['%Y-%m-%dT%H:%M']))

@register.filter(name='addclass4')
def addclass4(value, arg):
    argo = "input-text##" + "-" + '##' + 'text'
    arg_list = argo.split('##')
    return value.as_widget(attrs={'class': arg_list[0], 'type': arg_list[2]},
                           widget=forms.widgets.DateInput(attrs={'type': 'date', 'value': arg,}, format=('%Y-%m-%d')))


@register.filter(name='datetimedo')
def datetimedo(value):
    if not value.label == 'Updated at user':
        return value
    else:
        print(value.label)
        # return value.as_widget(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}, format=['%Y-%m-%dT%H:%M']))
        return value.as_widget(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}))


# @register.filter(name='addclass5')
# def addclass5(value, arg):
#     argo = "input-text##" + "-" + '##' + 'text'
#     arg_list = argo.split('##')
#     arg2 = [i[0] for i in arg]
#     print(arg2)
#     return value.as_widget(widget=Select2Multiple())

@register.simple_tag
def minis(obj):
    ans = obj - 1
    return ans

@register.simple_tag
def minispage(obj):
    if obj == 0:
        return obj
    else:
        ans = obj - 1
        return ans


@register.simple_tag
def pluspage(obj, max):
    if obj+1 == max:
        return obj
    else:
        ans = obj + 1
        return ans



@register.simple_tag
def chnorm(obj):
    ans = obj.get_short_name()
    return ans

@register.simple_tag
def save2(obj):
    print(obj)
    return str(obj)


@register.simple_tag
def datato(obj):
    obj2 = obj.lower()
    obj3 = obj2[:4]
    obj4 = obj2[-1]
    ans = obj3 + "_" + obj4
    return ans


@register.simple_tag
def isstriked(obj, striked):
    if striked:
        obj2 = obj + " " + "strike"
    else:
        obj2 = obj
    return obj2


@register.simple_tag
def refuse(obj):
    obj2 = "-" + obj
    return obj2

@register.simple_tag
def as2(obj):
    a = obj[-7:-4]
    return a


@register.simple_tag
def multichfirst(obj):
    if obj is not None:
        if obj.startswith("['") and obj.endswith("']"):
            a1 = obj.strip('[]')
            a2 = a1.strip("'")
            a3 = a2.replace("', '", ";\n")
            return a3
        else:
            return obj
    else:
        return None


@register.simple_tag
def cont(obj, obj2):
    a = obj + obj2
    return a


