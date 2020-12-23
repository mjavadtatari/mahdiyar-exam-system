import random
import string
import time
import uuid
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import Group, Permission, AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from jalali_date import date2jalali
from django.db.models import Q


class User(AbstractUser):
    """
    Adding more code to Django's User model!
    """

    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)

    IS_BOY = 1
    IS_GIRL = 2
    GENDER_TYPE = (
        (IS_BOY, 'پسر'),
        (IS_GIRL, 'دختر'),
    )
    gender = models.SmallIntegerField(choices=GENDER_TYPE, default=1, null=True, blank=True)

    def __str__(self):
        return '{} ------ با نام کاربری {}'.format(self.get_full_name(), self.username)

    def user_type_is(self):
        if self.is_student:
            return 'دانش آموز'
        elif self.is_teacher:
            return 'آموزگار'
        elif self.is_supervisor:
            return 'سرپرست'
        elif self.is_superuser:
            return 'ادمین'


class Klass(models.Model):
    """
    representing a model for an academy' class
    """

    class Meta:
        verbose_name = "کلاس"
        verbose_name_plural = "کلاس"

    name = models.CharField(max_length=100, verbose_name="نام کلاس")
    academy = models.ForeignKey(to='dashboard.Academy', on_delete=models.CASCADE, verbose_name="آموزشگاه")
    subject = models.ForeignKey(to='dashboard.Category', on_delete=models.DO_NOTHING,
                                verbose_name="پایه تحصیلی")
    teacher = models.ManyToManyField(to='dashboard.Profile', verbose_name="آموزگار (ها)", related_name='klass_teacher')

    def __str__(self):
        return '{} - {}'.format(self.name, self.academy.name)


class Academy(models.Model):
    """
    representing a model for an academy
    """

    class Meta:
        verbose_name = "آموزشگاه"
        verbose_name_plural = "آموزشگاه"

    name = models.CharField(max_length=300, verbose_name="نام آموزشگاه")
    phone = models.CharField(max_length=11, verbose_name="تلفن آموزشگاه", blank=True, null=True)
    address = models.TextField(verbose_name="آدرس آموزشگاه", blank=True, null=True)

    def __str__(self):
        return '{}'.format(self._meta.verbose_name + ' ' + self.name)


class Profile(models.Model):
    """
    Representing base profile(dashboard) for all users!
    """

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل"

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="حساب کاربری")
    passport_number = models.CharField(max_length=10, verbose_name="کد ملی", blank=True, null=True, default=' ')
    phone_number = models.CharField(max_length=11, verbose_name="تلفن همراه", blank=True, null=True, default='0')
    birth_date = models.DateField(null=True, blank=True, verbose_name="تاریخ تولد", default='2020-02-20')
    profile_image = models.ImageField(verbose_name="نمایه کاربری", upload_to='users/profile_images/', null=True,
                                      blank=True)
    academy = models.ForeignKey(to='dashboard.Academy', on_delete=models.DO_NOTHING, verbose_name="آموزشگاه",
                                null=True)
    klass = models.ManyToManyField(to='dashboard.Klass', verbose_name="کلاس")

    def __str__(self):
        return '{} {}'.format(self.user.user_type_is(), self.user.get_full_name())

    def show_birth_date_in_jalali(self):
        return date2jalali(self.birth_date).strftime('%Y/%m/%d')

    def get_wallet(self):
        return Wallet.objects.get(user=self.user)

    def user_type_finder(self):
        answer = ""
        temp_flag = False
        if self.user.is_superuser:
            answer += "ادمین سایت"
            temp_flag = True
        if self.user.is_teacher:
            if temp_flag:
                answer += " و "
            answer += "آموزگار"
            temp_flag = True
        if self.user.is_student:
            if temp_flag:
                answer += " و "
            answer += "دانش آموز"
            temp_flag = True
        if self.user.is_supervisor:
            if temp_flag:
                answer += " و "
            answer += "سرپرست"
        return answer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        if instance.profile.user.is_student:
            student_permissions = Permission.objects.filter(
                Q(codename='view_exam') | Q(codename='view_choice') | Q(codename='view_question') | Q(
                    codename='view_studentscore') | Q(codename='add_studentanswer') | Q(
                    codename='change_studentanswer'))
            student_permissions = list(i for i in student_permissions)
            for i in student_permissions:
                instance.user_permissions.add(i)
            instance.save()
        elif instance.profile.user.is_teacher:
            Wallet.objects.create(user=instance)
            teacher_permissions = Permission.objects.filter(
                Q(codename__contains='exam') | Q(codename__contains='choice') | Q(codename__contains='question') | Q(
                    codename='view_studentscore') | Q(codename='view_studentanswer') | Q(codename='view_student') | Q(
                    codename='view_transaction') | Q(codename='add_transaction') | Q(
                    codename='view_wallet'))
            teacher_permissions = list(i for i in teacher_permissions)
            for i in teacher_permissions:
                instance.user_permissions.add(i)
            instance.save()
        elif instance.profile.user.is_supervisor:
            Wallet.objects.create(user=instance)
            supervisor_permissions = Permission.objects.filter(
                Q(codename__contains='exam') | Q(codename__contains='choice') | Q(codename__contains='question') | Q(
                    codename__contains='user') | Q(
                    codename__contains='studentscore') | Q(codename__contains='studentanswer') | Q(
                    codename__contains='klass') | Q(codename='view_transaction') | Q(codename='add_transaction') | Q(
                    codename='view_wallet'))
            supervisor_permissions = list(i for i in supervisor_permissions)
            for i in supervisor_permissions:
                instance.user_permissions.add(i)
            instance.save()
    instance.profile.save()


class StudentScore(models.Model):
    class Meta:
        verbose_name = "نمره"
        verbose_name_plural = "نمره"

    student = models.ForeignKey(to='dashboard.Profile', on_delete=models.CASCADE, verbose_name="دانش آموز")
    exam = models.ForeignKey(to='dashboard.Exam', on_delete=models.CASCADE, verbose_name="آزمون")
    all_questions = models.IntegerField(verbose_name="تعداد سوالات پاسخ داده")
    score = models.FloatField(verbose_name="نمره")
    percentage = models.FloatField(verbose_name="درصد")

    def __str__(self):
        return '{} - {} - {}'.format(self.student.user.get_full_name(), self.exam.exam_name, self.score)


def show_notification():
    output = []
    temp_y = 10
    temp_x = Notification.objects.filter(show_on_dashboard=True).order_by('-date')
    if len(temp_x) < 10:
        temp_y = len(temp_x)
    for i in range(0, temp_y):
        output.append(temp_x[i])
    return temp_x


class Notification(models.Model):
    class Meta:
        verbose_name = "اطلاعیه"
        verbose_name_plural = "اطلاعیه"

    RED = 'danger'
    BLUE = 'info'
    YELLOW = 'warning'
    GREEN = 'success'
    COLOR_CHOICES = (
        (RED, 'قرمز'),
        (BLUE, 'آبی'),
        (YELLOW, 'زرد'),
        (GREEN, 'سبز'),
    )
    color = models.CharField(max_length=10, default=RED, choices=COLOR_CHOICES, verbose_name="رنگ اطلاعیه")
    show_on_login = models.BooleanField(verbose_name='نمایش در صفحه ورود', default=False)
    show_on_signup = models.BooleanField(verbose_name='نمایش در صفحه ثبت نام', default=False)
    show_on_dashboard = models.BooleanField(verbose_name='نمایش در داشبورد', default=False)
    notification_title = models.CharField(max_length=300, verbose_name="عنوان")
    notification_text = models.TextField(verbose_name="متن", null=True, blank=True)
    notification_image = models.ImageField(upload_to='notification_pics/', null=True, blank=True, verbose_name="تصویر")
    date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return '{}'.format(self.notification_title)


class Category(models.Model):
    """
    for sorting students, teachers and academies!
    """
    name = models.CharField(max_length=250, verbose_name="نام دسته")
    slug = models.SlugField(verbose_name="لینک دسته", unique=True,
                            help_text="از یک کلمه به زبان انگلیسی استفاده کنید! مثال: ریاضی - riazi")
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True,
                               verbose_name="دسته پایه",
                               help_text="اگر قصد ایجاد زیر دسته را دارید، دسته والد را از این قسمت انتخاب کنید در غیر اینصورت فیلد را تغییر ندهید!")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی"
        # enforcing that there can not be two categories under a parent with same slug
        unique_together = ('slug', 'parent')
        # ordering = ('',)

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Question(models.Model):
    """
    Representing a Model as Base, fot Multi Choices and True/False Questions model
    """

    class Meta:
        verbose_name = "سوال"
        verbose_name_plural = "سوال"
        ordering = ('-publish_date',)

    question_label = models.TextField(verbose_name="صورت سوال")
    is_active = models.BooleanField(default=True, verbose_name="وضعیت سوال", help_text="آیا سوال فعال باشد؟")
    category = models.ForeignKey(to='dashboard.Category', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name="دسته بندی")
    question_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    creator = models.ForeignKey(to='dashboard.Profile', on_delete=models.CASCADE, verbose_name="طراح سوال",
                                null=True)
    question_picture = models.ImageField(upload_to='questions_pics/', null=True, blank=True, verbose_name="تصویر سوال")
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ انتشار")

    def __str__(self):
        return self.question_label[:50] + " ..."

    def get_category_list(self):
        k = self.category
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb) - 1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i - 1:-1])
        return breadcrumb[-1:0:-1]


class Choice(models.Model):
    """
    Representing a model for making Multi Choices Question Options
    """

    choice_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    choice_position = models.IntegerField(verbose_name="شماره گزینه")
    choice_question = models.ForeignKey(to='dashboard.Question', on_delete=models.CASCADE, verbose_name="سوال")
    choice_label = models.CharField(max_length=1000, verbose_name="متن گزینه")
    is_correct = models.BooleanField(default=False, verbose_name="این گزینه صحیح است؟",
                                     help_text="تنها برای گزینه صحیح (بله) و برای سایر گزینه ها (خیر) را انتخاب نمایید!")

    class Meta:
        verbose_name = "گزينه"
        verbose_name_plural = "گزينه"
        unique_together = [
            # no duplicated choice per question
            ("choice_question", "choice_label"),
            ("choice_question", "choice_id"),
            # no duplicated position per question
            ("choice_question", "choice_position")
        ]
        ordering = ('choice_question',)

    def __str__(self):
        return 'گزینه: {} --- برای سوال: {} '.format(self.choice_label, self.choice_question.question_label[:50])


class StudentAnswer(models.Model):
    """
    Representing a model for students answer
    """

    class Meta:
        verbose_name = "پاسخ دانش آموز"
        verbose_name_plural = "پاسخ دانش آموز"

    student = models.ForeignKey(to='dashboard.Profile', on_delete=models.CASCADE, verbose_name="دانش آموز")
    question = models.ForeignKey(to='dashboard.Question', on_delete=models.CASCADE, verbose_name="آزمون")
    answer_time = models.DateTimeField(null=True, verbose_name="تاریخ و زمان پاسخ دهی")
    answer_option = models.ForeignKey('Choice', on_delete=models.CASCADE, blank=True, null=True,
                                      verbose_name="پاسخ دانش آموز")


class Exam(models.Model):
    """
    Representing a model for exam objects
    """

    class Meta:
        verbose_name = "آزمون"
        verbose_name_plural = "آزمون"

    exam_name = models.CharField(max_length=300, verbose_name="عنوان آزمون")
    exam_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    exam_klass = models.ForeignKey(to='dashboard.Klass', on_delete=models.DO_NOTHING, verbose_name="کلاس")
    exam_duration = models.DurationField(verbose_name="مدت زمان آزمون",
                                         help_text="به عنوان مثال برای 20 دقیقه، 00:20:00 را وارد کنید!")
    exam_start = models.DateTimeField(verbose_name="تاریخ شروع")
    exam_finish = models.DateTimeField(verbose_name="تاریخ پایان")
    exam_question = models.ManyToManyField(Question, verbose_name="سوالات آزمون",
                                           help_text="همه سوال های مورد نظر برای قرار گیری در آزمون را انتخاب کنید ")
    is_active = models.BooleanField(default=True, verbose_name="آزمون فعال است؟")
    exam_creator = models.ForeignKey(to='dashboard.Profile', on_delete=models.CASCADE, verbose_name="طراح آزمون",
                                     null=True)
    exam_guide = models.TextField(null=True, blank=True, verbose_name="توضیحات آزمون",
                                  help_text="راهنمایی برای دانش آموزان (اختیاری)")

    def __str__(self):
        return '{}'.format(self.exam_name)

    def update_exam_status(self):
        now_time = datetime.now()
        if now_time > self.exam_finish and self.is_active:
            self.is_active = False
        self.save()


class ExamPerStudent(models.Model):
    """
    a model for saving question's order and remaining time for each student taking the exam!
    """

    class Meta:
        verbose_name = 'آزمون دانش آموز'
        verbose_name_plural = 'آزمون دانش آموز'

    student = models.ForeignKey(to='dashboard.Profile', on_delete=models.CASCADE)
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
    STU_start = models.DateTimeField(null=True)  # when student start the exam
    STU_finish = models.DateTimeField(null=True)  # when student supposed to finish the exam
    STU_remain_time = models.DurationField(null=True)
    STU_questions = ArrayField(base_field=models.UUIDField(null=True))
    STU_answers = ArrayField(base_field=models.UUIDField(null=True), blank=True)

    def __str__(self):
        return 'آزمون {} - {}'.format(self.exam, self.student)

    def modify_answers(self):
        for i in self.STU_questions:
            temp_object = StudentAnswer.objects.create(question_id=i, exam=self.exam, student=self.student)
            self.STU_answers.append(temp_object.pk)
        self.save()

    def calculate_finish_date_time(self):
        self.STU_finish = self.STU_start + self.exam.exam_duration
        self.STU_remain_time = self.exam.exam_duration
        self.save()

    def update_remain_time(self, entry=None):
        if entry:
            self.STU_remain_time = self.STU_finish - self.STU_finish
            remain = self.STU_remain_time
            self.save()
            return remain.total_seconds()
        elif self.STU_remain_time.total_seconds() <= 0:
            return -1
        else:
            now_time = datetime.now()
            if now_time >= self.STU_finish:
                self.STU_remain_time = 0
                return -1
            remain = self.STU_finish - now_time
            self.STU_remain_time = remain
        self.save()
        return remain.total_seconds()

    def calculate_the_score(self):
        temp_choices = self.STU_answers
        all_choices = []
        for i in temp_choices:
            if Choice.objects.filter(pk=i).count() == 0:
                continue
            else:
                all_choices.append(Choice.objects.get(pk=i))

        right_answers = []
        score = 0
        total_score = len(all_choices)
        for i in all_choices:
            if i.is_correct:
                right_answers.append(i)
                score += 1
        if total_score == 0:
            percentage = 0
        else:
            percentage = (score * 100) / self.exam.exam_question.count()
        return StudentScore.objects.create(student=self.student, exam=self.exam, all_questions=len(all_choices),
                                           score=score,
                                           percentage=percentage)

    def re_calculate_the_score(self):
        try:
            temp_score = StudentScore.objects.get(student=self.student, exam=self.exam)
            temp_score.delete()
            self.calculate_the_score()
        except ObjectDoesNotExist:
            pass

    def save_answer(self, question, answer):
        if answer is None:
            answer = '00000000-0000-0000-0000-000000000000'
        temp_q_list = self.STU_questions
        temp_a_list = self.STU_answers

        for i in range(len(temp_q_list)):
            if temp_q_list[i] == uuid.UUID(question):
                temp_a_list[i] = uuid.UUID(answer)

        self.save()


class Wallet(models.Model):
    """
    representing a wallet for supervisors and teachers
    """

    class Meta:
        verbose_name = "کیف پول"
        verbose_name_plural = "کیف پول"

    user = models.OneToOneField(to='dashboard.User', on_delete=models.CASCADE, verbose_name="حساب کاربری")
    balance = models.IntegerField(default=0, verbose_name="اعتبار")

    def __str__(self):
        return 'کیف پول کاربر {}'.format(self.user.get_full_name())

    def get_balance(self):
        return '{} آزمون'.format(self.balance)

    def spend(self, amount, description=None):
        if self.balance < amount:
            return False
        self.balance -= amount
        self.save()
        Transaction.objects.create(wallet=self, amount=amount, transaction_type=2, description=description)
        return True

    def deposit(self, amount, description=None):
        self.balance += amount
        self.save()
        Transaction.objects.create(wallet=self, amount=amount, transaction_type=1, description=description)

    def transfer_to_teacher(self, amount, other_user):
        if self.balance < amount:
            return False
        self.spend(amount=amount, description='واریز به: ' + other_user.user.get_full_name())
        other_user.deposit(amount=amount, description='از طرف: ' + self.user.get_full_name())
        return True


class Transaction(models.Model):
    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش"

    wallet = models.ForeignKey(to='dashboard.Wallet', on_delete=models.CASCADE, verbose_name="کیف پول")
    order_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان تراکنش")
    amount = models.IntegerField(verbose_name="مبلغ")
    description = models.TextField(verbose_name="توضیحات", null=True, blank=True)

    DEPOSIT = 1
    SPEND = 2
    TRANSACTION_CHOICES = (
        (DEPOSIT, "افزودن"),
        (SPEND, "خرج کردن"),
    )
    transaction_type = models.SmallIntegerField(choices=TRANSACTION_CHOICES, verbose_name="نوع تراکنش")

    def __str__(self):
        return '{} - {}'.format(self.wallet.user.get_full_name(), self.amount)

    def get_amount(self):
        return '{} آزمون'.format(self.amount)

    def get_amount_in_list(self):
        return '{}'.format(self.amount)


def create_exam_per_student(student, exam):
    all_questions = Question.objects.filter(exam=exam)
    all_questions = list(i for i in all_questions)
    random.shuffle(all_questions)
    all_answers = []
    for i in all_questions:
        x = StudentAnswer.objects.create(student=student, question=i)
        all_answers.append(x)

    send_question = [i.pk for i in all_questions]
    send_answer = [i.pk for i in all_answers]

    return ExamPerStudent.objects.create(student=student, exam=exam, STU_questions=send_question,
                                         STU_answers=send_answer)


def is_first_time(student, exam):
    temp_result = ExamPerStudent.objects.filter(student=student, exam=exam)
    temp_result = list(i for i in temp_result)
    if len(temp_result) == 0:
        return True
    else:
        return False


def is_start_time(exam):
    now_time = datetime.now()
    if now_time <= exam.exam_start or now_time >= exam.exam_finish:
        return False
    else:
        return True


def is_exam_time(exam):
    now_time = datetime.now()
    if now_time <= exam.exam_start:
        return -1  # not started yet
    elif now_time >= exam.exam_finish:
        return 1  # exam finished
    else:
        return 0  # now available


def get_random_string(length):
    result_str = ''
    for i in range(length):
        rand_x = random.randint(0, 10)
        if rand_x % 2 == 0:
            if rand_x <= 4:
                letters = string.ascii_uppercase
            else:
                letters = string.ascii_lowercase
            temp_letter = random.choice(letters)
        else:
            temp_letter = str(random.randint(0, 10))
        result_str += temp_letter

    return result_str


class SignUpKey(models.Model):
    sign_up_key = models.CharField(verbose_name='کلید ثبت نام', default=get_random_string(8), primary_key=True,
                                   editable=False, unique=True, max_length=10)
    klass = models.OneToOneField(to='dashboard.Klass', verbose_name='کلاس', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'کلید ثبت نام'
        verbose_name_plural = 'کلید ثبت نام'
        unique_together = ('sign_up_key', 'klass')


@receiver(post_save, sender='dashboard.Klass')
def create_klass_signup_key(sender, instance, created, **kwargs):
    if created:
        while True:
            temp_signup_key = SignUpKey.objects.create(klass=instance)
            if temp_signup_key:
                break
