from django import forms as form
from django.forms import *
from company.models import Employe, Benefit
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML, ButtonHolder
from crispy_forms.bootstrap import InlineField


class ProfileEditForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Field('name'),
            Field('surname'),
            HTML("<b>Kredi</b>"),
            InlineField('credit', readonly=True),
            Field('image'),
            HTML(
                """{% if form.image.value %}<img class="img-profile" src="{{ MEDIA_URL }}{{ form.image.value }}">{% endif %}"""),
            ButtonHolder(
                Submit('Save', 'Guncelle', css_class='button white'),
                HTML('<a class="btn btn-warning" href={% url "credit_transfer" %}>Kredi Transfer Et</a>'),
            )
        )

    class Meta:
        model = Employe
        fields = ['name', 'surname', 'credit', 'image']


class CreditTransferForm(Form):
    username = form.CharField()
    credit = form.IntegerField()

    def __init__(self, *args, **kwargs):
        super(CreditTransferForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit', 'Gonder'))


class ServiceUseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceUseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Kaydet'))

    class Meta:
        model = Benefit
        fields = ('usage',)

    def save(self, **kwargs):
        benefit = super(ServiceUseForm, self).save(commit=False)
        service = kwargs.get("service")
        employe = kwargs.get('employe')
        usage = kwargs.get('usage')
        if Benefit.objects.filter(employe_id=employe.id, service_id=service.id).exists():
            used_benefit = Benefit.objects.get(employe_id=employe.id, service_id=service.id)
            used_benefit.usage += usage
            used_benefit.save()
            employe.credit -= (service.credit * usage)
            employe.save()
        else:
            benefit.employe_id = employe.id
            benefit.service_id = service.id
            benefit.save()
            service = kwargs.get('service')
            employe.credit -= (service.credit * usage)
            employe.save()


class ServiceLeaveForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceLeaveForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Kaydet'))

    class Meta:
        model = Benefit
        fields = ('usage',)

    def save(self, **kwargs):
        benefit = super(ServiceLeaveForm, self).save(commit=False)
        service = kwargs.get("service")
        employe = kwargs.get('employe')
        usage = kwargs.get('usage')
        benefit = Benefit.objects.get(employe_id=employe.id, service_id=service.id)
        benefit.usage -= usage
        benefit.save()
        employe.credit += (service.credit * usage)
        employe.save()
