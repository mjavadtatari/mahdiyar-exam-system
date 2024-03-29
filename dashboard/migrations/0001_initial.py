# Generated by Django 3.1.1 on 2020-10-21 23:56

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_student', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
                ('is_supervisor', models.BooleanField(default=False)),
                ('gender', models.SmallIntegerField(blank=True, choices=[(1, 'پسر'), (2, 'دختر')], default=1, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Academy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='نام آموزشگاه')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='تلفن آموزشگاه')),
                ('address', models.TextField(blank=True, null=True, verbose_name='آدرس آموزشگاه')),
            ],
            options={
                'verbose_name': 'آموزشگاه',
                'verbose_name_plural': 'آموزشگاه',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='نام دسته')),
                ('slug', models.SlugField(help_text='از یک کلمه به زبان انگلیسی استفاده کنید! مثال: ریاضی - riazi', unique=True, verbose_name='لینک دسته')),
                ('parent', models.ForeignKey(blank=True, help_text='اگر قصد ایجاد زیر دسته را دارید، دسته والد را از این قسمت انتخاب کنید در غیر اینصورت فیلد را تغییر ندهید!', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.category', verbose_name='دسته پایه')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی',
                'unique_together': {('slug', 'parent')},
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('choice_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('choice_position', models.IntegerField(verbose_name='شماره گزینه')),
                ('choice_label', models.CharField(max_length=1000, verbose_name='متن گزینه')),
                ('is_correct', models.BooleanField(default=False, help_text='تنها برای گزینه صحیح (بله) و برای سایر گزینه ها (خیر) را انتخاب نمایید!', verbose_name='این گزینه صحیح است؟')),
            ],
            options={
                'verbose_name': 'گزينه',
                'verbose_name_plural': 'گزينه',
                'ordering': ('choice_question',),
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('exam_name', models.CharField(max_length=300, verbose_name='عنوان آزمون')),
                ('exam_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('exam_duration', models.DurationField(help_text='به عنوان مثال برای 20 دقیقه، 00:20:00 را وارد کنید!', verbose_name='مدت زمان آزمون')),
                ('exam_start', models.DateTimeField(verbose_name='تاریخ شروع')),
                ('exam_finish', models.DateTimeField(verbose_name='تاریخ پایان')),
                ('is_active', models.BooleanField(default=True, verbose_name='آزمون فعال است؟')),
                ('exam_guide', models.TextField(blank=True, help_text='راهنمایی برای دانش آموزان (اختیاری)', null=True, verbose_name='توضیحات آزمون')),
            ],
            options={
                'verbose_name': 'آزمون',
                'verbose_name_plural': 'آزمون',
            },
        ),
        migrations.CreateModel(
            name='Klass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام کلاس')),
                ('academy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.academy', verbose_name='آموزشگاه')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.category', verbose_name='پایه تحصیلی')),
            ],
            options={
                'verbose_name': 'کلاس',
                'verbose_name_plural': 'کلاس',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('danger', 'قرمز'), ('info', 'آبی'), ('warning', 'زرد'), ('success', 'سبز')], default='danger', max_length=10, verbose_name='رنگ اطلاعیه')),
                ('title', models.CharField(max_length=300, verbose_name='عنوان')),
                ('text', models.TextField(verbose_name='متن')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'اطلاعیه',
                'verbose_name_plural': 'اطلاعیه',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passport_number', models.CharField(blank=True, default=' ', max_length=10, null=True, verbose_name='کد ملی')),
                ('phone_number', models.CharField(blank=True, default='0', max_length=11, null=True, verbose_name='تلفن همراه')),
                ('birth_date', models.DateField(blank=True, default='2020-02-20', null=True, verbose_name='تاریخ تولد')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='users/profile_images/', verbose_name='نمایه کاربری')),
                ('academy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.academy', verbose_name='آموزشگاه')),
                ('klass', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.klass', verbose_name='کلاس')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='حساب کاربری')),
            ],
            options={
                'verbose_name': 'پروفایل',
                'verbose_name_plural': 'پروفایل',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_label', models.TextField(verbose_name='صورت سوال')),
                ('is_active', models.BooleanField(default=True, help_text='آیا سوال فعال باشد؟', verbose_name='وضعیت سوال')),
                ('question_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('question_picture', models.ImageField(blank=True, null=True, upload_to='questions_pics/', verbose_name='تصویر سوال')),
                ('publish_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.category', verbose_name='دسته بندی')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.profile', verbose_name='طراح سوال')),
            ],
            options={
                'verbose_name': 'سوال',
                'verbose_name_plural': 'سوال',
                'ordering': ('-publish_date',),
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.IntegerField(default=0, verbose_name='اعتبار')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='حساب کاربری')),
            ],
            options={
                'verbose_name': 'کیف پول',
                'verbose_name_plural': 'کیف پول',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان تراکنش')),
                ('amount', models.IntegerField(verbose_name='مبلغ')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('transaction_type', models.SmallIntegerField(choices=[(1, 'افزودن'), (2, 'خرج کردن')], verbose_name='نوع تراکنش')),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.wallet', verbose_name='کیف پول')),
            ],
            options={
                'verbose_name': 'تراکنش',
                'verbose_name_plural': 'تراکنش',
            },
        ),
        migrations.CreateModel(
            name='StudentScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('all_questions', models.IntegerField(verbose_name='تعداد سوالات پاسخ داده')),
                ('score', models.FloatField(verbose_name='نمره')),
                ('percentage', models.FloatField(verbose_name='درصد')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.exam', verbose_name='آزمون')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.profile', verbose_name='دانش آموز')),
            ],
            options={
                'verbose_name': 'نمره',
                'verbose_name_plural': 'نمره',
            },
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_time', models.DateTimeField(null=True, verbose_name='تاریخ و زمان پاسخ دهی')),
                ('answer_option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.choice', verbose_name='پاسخ دانش آموز')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.question', verbose_name='آزمون')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.profile', verbose_name='دانش آموز')),
            ],
            options={
                'verbose_name': 'پاسخ دانش آموز',
                'verbose_name_plural': 'پاسخ دانش آموز',
            },
        ),
        migrations.AddField(
            model_name='klass',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='klass_teacher', to='dashboard.profile', verbose_name='آموزگار'),
        ),
        migrations.CreateModel(
            name='ExamPerStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('STU_start', models.DateTimeField(null=True)),
                ('STU_finish', models.DateTimeField(null=True)),
                ('STU_remain_time', models.DurationField(null=True)),
                ('STU_questions', django.contrib.postgres.fields.ArrayField(base_field=models.UUIDField(null=True), size=None)),
                ('STU_answers', django.contrib.postgres.fields.ArrayField(base_field=models.UUIDField(null=True), blank=True, size=None)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.profile')),
            ],
            options={
                'verbose_name': 'آزمون دانش آموز',
                'verbose_name_plural': 'آزمون دانش آموز',
            },
        ),
        migrations.AddField(
            model_name='exam',
            name='exam_creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.profile', verbose_name='طراح آزمون'),
        ),
        migrations.AddField(
            model_name='exam',
            name='exam_klass',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.klass', verbose_name='کلاس'),
        ),
        migrations.AddField(
            model_name='exam',
            name='exam_question',
            field=models.ManyToManyField(help_text='همه سوال های مورد نظر برای قرار گیری در آزمون را انتخاب کنید ', to='dashboard.Question', verbose_name='سوالات آزمون'),
        ),
        migrations.AddField(
            model_name='choice',
            name='choice_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.question', verbose_name='سوال'),
        ),
        migrations.CreateModel(
            name='SignUpKey',
            fields=[
                ('sign_up_key', models.CharField(default='ZFxCj5I10', editable=False, max_length=10, primary_key=True, serialize=False, unique=True, verbose_name='کلید ثبت نام')),
                ('klass', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.klass', verbose_name='کلاس')),
            ],
            options={
                'verbose_name': 'کلید ثبت نام',
                'verbose_name_plural': 'کلید ثبت نام',
                'unique_together': {('sign_up_key', 'klass')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='choice',
            unique_together={('choice_question', 'choice_position'), ('choice_question', 'choice_label'), ('choice_question', 'choice_id')},
        ),
    ]
