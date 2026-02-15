"""real_time_mock_interview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from mock_interview_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('log',views.log),
    path('admin_home',views.admin_home),
    path('approved_company',views.approved_company),
    path('company_and_approve',views.company_and_approve),
    path('company_review/<id>',views.company_review),
    path('placed_candidates',views.placed_candidates),
    path('rejected_company',views.rejected_company),
    path('vaccency_list/<id>',views.vaccency_list),
    path('login_post',views.login_post),
    path('approve_company/<id>',views.approve_company),
    path('reject_company/<id>', views.reject_company),
    path('change_password',views.change_password),
    path('company_home',views.compay_home),
    path('compay_home',views.compay_home),
    path('company_reg',views.company_reg),
    # path('edit_profile',views.edit_profile),
    path('edit_question',views.edit_question),
    path('edit_vacancy/<id>',views.edit_vacancy),
    path('question_add',views.question_add),
    path('vacancy',views.vacancy),
    path('view_candidates/<id>',views.view_candidates),
    path('view_profile',views.view_profile),
    path('view_question/<id>',views.view_question),
    path('change_password_post',views.change_password_post),
    # path(' edit_profile_post',views. edit_profile_post),
    path('edit_question_post',views.edit_question_post),
    path('edit_vacancy_post/<id>',views.edit_vacancy_post),
    path('question_add/<id>',views.question_add),
    path('vacancy_post',views.vacancy_post),
    path('logout',views.logout),
    path('view_vacency',views.view_vacency),
    path('delete_vacency/<id>',views.delete_vacency),
    path('question_add_post/<id>',views.question_add_post),
    path('company_reg_post',views.company_reg_post),
    path('edit_profile_update/<id>',views.edit_profile_update),
    path('schedule_test/<id>',views.schedule_test),
    path('schedule_test_post/<id>',views.schedule_test_post),
    path('view_shortlist_candidates',views.view_shortlist_candidates),
    path('schedule_interview/<id>',views.schedule_interview),
    path('schedule_interview_post/<id>',views.schedule_interview_post),
    path('mark_candidates/<id>',views.mark_candidates),
    path('edit_questions/<id>',views.edit_questions),
    path('edit_questions_post/<id>',views.edit_questions_post),
    path('delete_question/<id>',views.delete_question),
    path('chatt/<u>',views.chatt),
    path('chatsnd',views.chatsnd),
    path('chatrply',views.chatrply),
    path('change_pswd',views.change_pswd),
    path('review_company/<id>',views.review_company),
    path('user_home',views.user_home),
    path('user_login',views.user_login),
    path('signup',views.signup),
    path('view_profilee',views.view_profilee),
    path('view_company',views.view_company),
    path('applied_vacency',views.applied_vacency),
    path('final_result',views.final_result),
    # path('schedule_list',views.schedule_list),
    path('view_shortlisted_list',views.view_shortlisted_list),
    path('view_vacancy/<id>',views.view_vacancy),
    path('view_exam_date/<id>',views.view_exam_date),
    path('change_pswd_post',views.change_pswd_post),
    path('apply_vacency/<id>',views.apply_vacency),
    path('',views.main_index),
    path('signup_post', views.signup_post),
    path('review_post/<id>', views.review_post),
    path('view_sample_question/<id>', views.view_sample_question),
    path('play_newcam', views.play_newcam),
    path('handle_post/<id>', views.handle_post),
    path('company_view_applied_candidate', views.company_view_applied_candidate),
    path('chattt/<u>', views.chattt),
    path('chatsndd', views.chatsndd),
    path('chatrplyy', views.chatrplyy),
    # path('submit_answer/<id>', views.submit_answer),
    # path('play_newcam', views.play_newcam),
    # path('Attend_exam/<id>', views.Attend_exam),
    # path('exam_details/<id>', views.exam_details),




]
