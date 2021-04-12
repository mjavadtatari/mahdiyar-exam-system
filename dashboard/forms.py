from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.forms import formset_factory
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField, JalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime

from dashboard.models import *


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-user', 'placeholder': 'نام شما'}))
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-user', 'placeholder': 'نام کاربری'}))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-user', 'placeholder': 'نام خانوادگی شما'}))
    email = forms.EmailField(max_length=254, label='آدرس ایمیل',
                             error_messages={'invalid': 'آدرس ایمیل اشتباه وارد شده است'},
                             widget=forms.EmailInput(attrs={'class': 'form-control form-control-user',
                                                            'placeholder': 'آدرس ایمیل بدون www'}), required=False, )
    password1 = forms.CharField(strip=False, label='رمز عبور', required=True, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control form-control-user', 'placeholder': 'رمز عبور'}))
    password2 = forms.CharField(strip=False, label='تکرار رمز عبور', required=True, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control form-control-user',
               'placeholder': 'تکرار رمز عبور'}))

    error_messages = {'password_mismatch': 'رمز های عبور هم خوانی ندارند'}

    IS_STUDENT = 1
    IS_TEACHER = 2
    IS_SUPERVISOR = 3
    TYPE_CHOICES = [
        (IS_STUDENT, 'دانش آموز'),
        (IS_TEACHER, 'آموزگار'),
        (IS_SUPERVISOR, 'سرپرست (مدیریت)'),
    ]
    user_type = forms.IntegerField(required=True, label='سطح کاربری',
                                   widget=forms.RadioSelect(choices=TYPE_CHOICES,
                                                            attrs={'class': 'list-options-style'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_student', 'is_teacher',
                  'is_supervisor')


class SignUpKeyCheckerForm(forms.Form):
    sign_up_key = forms.CharField(label='کلید ثبت نام', max_length=15, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-user', 'placeholder': 'کلید ثبت نام'}))


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('passport_number', 'phone_number', 'birth_date', 'profile_image')
        widgets = {
            'passport_number': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ChangeProfileForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'] = JalaliDateField(label='birth_date', widget=AdminJalaliDateWidget(
            attrs={'class': 'form-control form-control-user'}))


class ChangeProfileUserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(strip=False, label='رمز عبور قدیمی', required=True, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control form-control-user'}))
    new_password1 = forms.CharField(strip=False, label='رمز عبور جدید', required=True, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control form-control-user'}))
    new_password2 = forms.CharField(strip=False, label='تکرار رمز عبور جدید', required=True, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control form-control-user'}))

    error_messages = {'password_mismatch': 'رمز های عبور هم خوانی ندارند',
                      'password_incorrect': 'رمز عبور قدیمی اشتباه است',
                      }

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class RegisterAcademyForm(forms.ModelForm):
    class Meta:
        model = Academy
        exclude = ['academy_manager', ]
        widgets = {
            'academy_name': forms.TextInput(attrs={'class': 'form-control'}),
            'academy_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'academy_subject': forms.Select(attrs={'class': 'form-control'}),
            'academy_address': forms.Textarea(attrs={'class': 'form-control'}),
        }


class RegisterKlassForm(forms.ModelForm):
    class Meta:
        model = Klass
        exclude = ['klass_academy', ]
        widgets = {
            'klass_name': forms.TextInput(attrs={'class': 'form-control'}),
            'klass_subject': forms.Select(attrs={'class': 'form-control'}),
        }


class CreateAcademy(forms.ModelForm):
    class Meta:
        model = Academy
        exclude = []
        widgets = {
            'academy_manager': forms.Select(attrs={'class': 'form-control'}),
            'academy_name': forms.TextInput(attrs={'class': 'form-control'}),
            'academy_subject': forms.Select(attrs={'class': 'form-control'}),
            'academy_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'academy_address': forms.Textarea(attrs={'class': 'form-control'}),
        }


class NotificationChangeForm(forms.ModelForm):
    class Meta:
        model = Notification
        exclude = ['date']
        widgets = {
            'color': forms.Select(attrs={'class': 'form-control'}),
            'notification_title': forms.TextInput(attrs={'class': 'form-control'}),
            'notification_text': forms.Textarea(attrs={'class': 'form-control'}),
            'notification_image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class AcademyChangeForm(forms.ModelForm):
    class Meta:
        model = Academy
        exclude = []
        widgets = {
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }


class KlassChangeForm(forms.ModelForm):
    class Meta:
        model = Klass
        exclude = []
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'academy': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'teacher': forms.CheckboxSelectMultiple(
                attrs={'class': 'overflow-auto custom-checkbox exam-question-selector'}),
        }

    def __init__(self, *args, **kwargs):
        super(KlassChangeForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].queryset = Profile.objects.filter(user__is_teacher=True)


class KlassAcademyChanger(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('klass',)
        widgets = {
            'klass': forms.Select(attrs={'class': 'form-control'}),
        }


class CreateExamForm(forms.ModelForm):
    exam_start = forms.DateTimeField(widget=AdminJalaliDateWidget, label='تاریخ شروع')
    exam_finish = forms.DateTimeField(widget=AdminJalaliDateWidget, label='تاریخ پایان')

    class Meta:
        model = Exam
        exclude = ['exam_id']
        widgets = {
            'exam_name': forms.TextInput(attrs={'class': 'form-control'}),
            'exam_klass': forms.Select(attrs={'class': 'form-control'}),
            'exam_duration': forms.TimeInput(attrs={'class': 'form-control'}),
            'exam_start': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'exam_finish': forms.DateTimeInput(attrs={'class': 'form-control'}),
            # 'exam_question': forms.SelectMultiple(attrs={'class': 'form-control min_height_question_selector'}),
            'exam_question': forms.CheckboxSelectMultiple(
                attrs={'class': 'overflow-auto custom-checkbox exam-question-selector'}),
            'exam_guide': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ChangeCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = []
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }


class ExamCreateForm(forms.ModelForm):
    class Meta:
        model = Exam
        exclude = ['exam_id', 'exam_creator']
        widgets = {
            'exam_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.NullBooleanSelect(attrs={'class': 'form-control'}),
            'exam_klass': forms.Select(attrs={'class': 'form-control'}),
            'exam_duration': forms.TimeInput(attrs={'class': 'form-control'}),
            'exam_question': forms.CheckboxSelectMultiple(
                attrs={'class': 'custom-checkbox'}),
            'exam_guide': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.q_maker = kwargs.pop('q_maker', None)
        super(ExamCreateForm, self).__init__(*args, **kwargs)
        self.fields['exam_start'] = JalaliDateField(
            widget=AdminJalaliDateWidget)
        self.fields['exam_finish'] = JalaliDateField(
            widget=AdminJalaliDateWidget)
        self.fields['exam_start'] = SplitJalaliDateTimeField(label="شروع آزمون", widget=AdminSplitJalaliDateTime)
        self.fields['exam_finish'] = SplitJalaliDateTimeField(label="پایان آزمون", widget=AdminSplitJalaliDateTime)
        self.fields['exam_question'].queryset = Question.objects.filter(creator=self.q_maker)
        if self.q_maker.user.is_supervisor:
            self.fields['exam_question'].queryset = Question.objects.filter(creator__academy=self.q_maker.academy)
            self.fields['exam_klass'].queryset = Klass.objects.filter(academy=self.q_maker.academy)
        else:
            self.fields['exam_question'].queryset = Question.objects.filter(creator=self.q_maker)
            self.fields['exam_klass'].queryset = Klass.objects.filter(teacher=self.q_maker)


class ExamChangeForm(forms.ModelForm):
    class Meta:
        model = Exam
        exclude = ['exam_id', 'exam_creator', 'exam_start', 'exam_finish']
        widgets = {
            'exam_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.NullBooleanSelect(attrs={'class': 'form-control'}),
            'exam_klass': forms.Select(attrs={'class': 'form-control'}),
            'exam_duration': forms.TimeInput(attrs={'class': 'form-control'}),
            'exam_question': forms.CheckboxSelectMultiple(
                attrs={'class': ' custom-checkbox exam-question-selector'}),
            'exam_guide': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.q_maker = kwargs.pop('q_maker', None)
        super(ExamChangeForm, self).__init__(*args, **kwargs)
        self.fields['exam_question'].queryset = Question.objects.filter(creator=self.q_maker)
        self.fields['exam_klass'].queryset = Klass.objects.filter(teacher=self.q_maker)


class QuestionChangeForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['question_id', 'publish_date', 'creator']
        widgets = {
            'question_label': forms.TextInput(attrs={'class': 'form-control'}),
            'question_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.NullBooleanSelect(attrs={'class': 'form-control'}),
        }

    # def __init__(self, *args, **kwargs):
    #     self.q_maker = kwargs.pop('q_maker', None)
    #     super(QuestionChangeForm, self).__init__(*args, **kwargs)
    #     self.fields['creator'].queryset = Question.objects.filter(creator=self.q_maker)


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['question_id', 'publish_date', 'creator']
        widgets = {
            'question_label': forms.TextInput(attrs={'class': 'form-control'}),
            'question_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.NullBooleanSelect(attrs={'class': 'form-control'}),
        }


class ChoiceChangeForm(forms.ModelForm):
    class Meta:
        model = Choice
        exclude = ['choice_question', 'choice_position', 'choice_id']
        widgets = {
            'choice_label': forms.TextInput(attrs={'class': 'form-control'}),
            'is_correct': forms.NullBooleanSelect(attrs={'class': 'form-control'}),
        }


ChoiceFormset = formset_factory(ChoiceChangeForm, extra=4)


# class AnotherChoiceFormset(BaseModelFormSet):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.queryset = Author.objects.filter(name__startswith='O')


class TakeExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        exclude = []


class TakeChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        exclude = []


class StudentAnswerForm(forms.ModelForm):
    class Meta:
        model = StudentAnswer
        exclude = ['student', 'question', 'answer_time']
        # widgets = {
        #     'answer_option': forms.RadioSelect(attrs={'class': ''}),
        # }

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question', None)
        super(StudentAnswerForm, self).__init__(*args, **kwargs)
        self.fields['answer_option'].queryset = Choice.objects.filter(choice_question=self.question)

    def show_question_choices(self):
        output = []
        for i in self.fields['answer_option'].queryset:
            x = {
                'item': i,
                'label': i.choice_label,
            }
            output.append(x)
        return output


class SupervisorFinderForm(forms.Form):
    supervisor = forms.ModelChoiceField(label='سرپرست', widget=forms.Select(attrs={'class': 'form-control'}),
                                        help_text="هر کاربر فقط میتواند سرپرست یک آموزشگاه باشد",
                                        queryset=Profile.objects.filter(user__is_supervisor=True))


class WalletIncreaseForm(forms.Form):
    amount = forms.IntegerField(label='میزان اعتبار', widget=forms.TextInput(attrs={'class': 'form-control'}))


class AcademyFinderForm(forms.Form):
    academy = forms.ModelChoiceField(label='آموزشگاه', widget=forms.Select(attrs={'class': 'form-control'}),
                                     queryset=Academy.objects.all())


class ImportStudentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.academy = kwargs.pop('academy')
        super(ImportStudentForm, self).__init__(*args, **kwargs)
        self.fields['klass'] = forms.ModelChoiceField(label='کلاس',
                                                      widget=forms.Select(attrs={'class': 'form-control'}),
                                                      queryset=Klass.objects.filter(academy=self.academy))

    klass = forms.ChoiceField(label='کلاس')
    exl_file = forms.FileField(label='فایل اکسل', widget=forms.FileInput(attrs={'class': 'form-control'}))


class ChangePasswordForm(forms.Form):
    password = forms.CharField(max_length=100, label='رمز عبور جدید',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))


class CopyObjectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CopyObjectForm, self).__init__(*args, **kwargs)
        self.fields['exam'] = forms.ModelChoiceField(label='از آزمون',
                                                     widget=forms.Select(attrs={'class': 'form-control'}),
                                                     queryset=Exam.objects.all())
        self.fields['klass'] = forms.ModelChoiceField(label='برای کلاس',
                                                      widget=forms.Select(attrs={'class': 'form-control'}),
                                                      queryset=Klass.objects.all())
