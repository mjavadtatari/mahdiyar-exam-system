from django.conf.urls import url
from django.urls import path, register_converter
from django.urls.converters import AcademyConverter, KlassConverter, PersonalConverter
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (

    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,

)

from dashboard import views

register_converter(AcademyConverter, 'academy_id')
register_converter(KlassConverter, 'klass_id')
register_converter(PersonalConverter, 'student_id')

app_name = 'dashboard'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('me/', views.me_view, name='me_view'),
    path('me/signupkey/', views.sign_up_key_view, name='sign_up_key'),
    path('me/edit/', views.profile_edit_view, name='profile_edit'),
    path('me/password/', views.password_edit_view, name='password_edit'),

    path('import/choose/', views.import_choose_view, name='import_choose'),
    path('import/students/<int:aca_id>/', views.import_student_view, name='import_student'),

    path('category/create/', views.category_create_view, name='category_create'),
    path('category/manage/', views.category_manage_view, name='category_manage'),
    path('category/change/<int:cat_id>/', views.category_change_view, name='category_change'),

    path('notification/create/', views.notification_create_view, name='notification_create'),
    path('notification/manage/', views.notification_manage_view, name='notification_manage'),
    path('notification/change/<int:ntf_id>/', views.notification_change_view, name='notification_change'),
    # path('notification/delete/<int:ntf_id>', views.notification_delete_view, name='notification_delete'),

    path('academy/create/', views.academy_create_view, name='academy_create'),
    path('academy/manage/', views.academy_manage_view, name='academy_manage'),
    path('academy/change/<int:aca_id>/', views.academy_change_view, name='academy_change'),
    # path('academy/delete/<int:aca_id>', views.academy_delete_view, name='academy_delete'),
    path('academy/view/<academy_id:aca_id>/', views.academy_view_view, name='academy_view'),

    path('klass/create/', views.klass_create_view, name='klass_create'),
    path('klass/manage/', views.klass_manage_view, name='klass_manage'),
    path('klass/change/<int:kls_id>/', views.klass_change_view, name='klass_change'),
    # path('klass/delete/<int:kls_id>', views.klass_delete_view, name='klass_delete'),
    path('klass/view/<klass_id:kls_id>/', views.klass_view_view, name='klass_view'),

    path('question/create/', views.question_create_view, name='question_create'),
    path('question/manage/', views.question_manage_view, name='question_manage'),
    path('question/change/<uuid:qes_id>/', views.question_change_view, name='question_change'),
    # path('question/delete/<uuid:qes_id>', views.question_delete_view, name='question_delete'),
    path('choice/change/<uuid:cho_id>/', views.choice_change_view, name='choice_change'),
    path('question/list/', views.question_list_view, name='question_list'),

    path('exam/create/', views.exam_create_view, name='exam_create'),
    path('exam/manage/', views.exam_manage_view, name='exam_manage'),
    path('exam/change/<uuid:exa_id>/', views.exam_change_view, name='exam_change'),
    # path('exam/delete/<uuid:exa_id>', views.exam_delete_view, name='exam_delete'),
    path('exam/info/<uuid:exa_id>/', views.exam_info_view, name='exam_info'),
    path('exam/start/<uuid:exa_id>/', views.exam_start_view, name='exam_start'),
    path('exam/end/<uuid:exa_id>/', views.exam_end_view, name='exam_end'),
    path('exam/examing/<uuid:exa_id>/', views.exam_examing_view, name='exam_examing'),
    path('exam/list/', views.exam_list_view, name='exam_list'),
    path('exam/score/', views.exam_score_view, name='exam_score'),
    path('exam/score/klass/<int:kls_id>/', views.supervisor_exam_klass_list_for_score_view,
         name='exam_klass_list_score'),
    path('exam/score/exam/<uuid:exa_id>/', views.supervisor_exam_list_for_score_view, name='exam_list_score'),
    path('exam/score/exam/<uuid:exa_id>/list/', views.supervisor_exam_score_list_view, name='exam_score_list'),
    path('exam/score/exam/<uuid:exa_id>/excel/', views.supervisor_exam_score_excel_view, name='exam_score_excel'),

    # path('exam/score/<uuid:exa_id>/', views.exam_score_list_supervisor_view, name='exam_score_list'),

    path('delete/<str:name>/<int:obj_id>/', views.delete_objects_view, name='delete_none_uuid'),
    path('delete/<str:name>/<uuid:obj_uuid>/', views.delete_uuid_objects_view, name='delete_uuid'),
    path('changepass/<str:name>/<int:user_id>/', views.changepass_user_view, name='changepass_user'),

    path('list/supervisor/', views.list_supervisor_view, name='list_supervisor'),
    path('list/teacher/', views.list_teacher_view, name='list_teacher'),
    path('list/student/', views.list_student_view, name='list_student'),
    path('list/all/<str:name>/', views.list_all_view, name='list_all'),

    path('copy/obj/<str:name>/', views.copy_object_view, name='copy_obj'),

    path('wallet/<int:wal_id>/', views.wallet_increase_view, name='wallet_increase'),
    path('wallet/transaction/list/', views.wallet_transaction_list_view, name='wallet_transaction_list'),


    path('admin/ec/score/', views.extra_exam_checker, name='extra_exam_checker'),
]
