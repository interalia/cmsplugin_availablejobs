# -*- coding: utf-8 -*-
from django import forms as form
from django.db import IntegrityError
from uni_form.helpers import FormHelper, Submit, Reset
from uni_form.helpers import Layout, Fieldset, Row, HTML
from uni_form.helpers import FormHelper, Submit
from models import Candidate
from django import forms

class ApplyForm(forms.Form):
    name = form.CharField(label="Nombre", help_text = "Escribe tu nombre completo")
    email = form.EmailField(help_text = u"Escribe tu email nombre@gmail.com")
    phone = form.CharField(help_text = u"Escribe tu teléfono", label=u"Mobile")
    cv= form.FileField(help_text = u"Anexa un archivo", label = "Curriculum")

    def get_candidate(self, op):
        name = self.cleaned_data["name"]
        email = self.cleaned_data["email"]
        phone = self.cleaned_data["phone"]
        cv = self.cleaned_data["cv_file"]
        candidate, created = Candidate.objects.get_or_create(name = name, email = email)
        if op:
            candidate.opening = op
        candidate.phone = phone
        candidate.cv = cv
        candidate.save()
        return candidate
   


