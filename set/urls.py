from django.urls import path
from . import views
urlpatterns = [
    path('', views.list_modules, name='list_modules'),
    path('modules/<int:module_pk>', views.module_sets_list, name='mudule_sets_list'),
    path('attempt-set/<int:set_pk>', views.attemp_set, name='attempt_set'),
    path('attempted-sets', views.attempted_sets, name='attempted_sets'),
    path('evaluate/<int:set_pk>', views.evaluate, name='evaluate'),
    path('result/<int:set_pk>', views.result, name='result'),

    # for admin
    path('admin-panel/modules/', views.admin_modules, name='admin-modules'),  # list of modules
    path('admin-panel/modules/add/', views.admin_add_module, name='add-module'),  # module add form
    path('admin-panel/modules/delete/', views.delete_module, name='delete-module'),  # delete module $
    path('admin-panel/modules/<int:module_pk>/sets/', views.admin_sets, name='admin-sets'),  # list of sets
    path('admin-panel/set/<int:set_pk>/', views.view_set, name='view-set'),  # set details and questions display for a particular set
    path('admin-panel/add_set/',views.add_set, name='add-set'),  # admin add set form plus basic details save to database via ajax
    path('admin-panel/set/<int:set_pk>/add-question/', views.add_question, name='add-question'),  # add question via ajax from add_set form
    path('admin-panel/delete_set/', views.delete_set, name='admin_delete_set'),  #  delete a particular set and its questions $
    path('admin-panel/delete_question/', views.delete_question, name='admin_delete_question'),  #  delete a particular set and its questions $
    path('admin-panel/attempted-sets/', views.admin_attempted_sets, name='attempted-sets-admin'),
    path('admin-panel/result/<int:set_pk>', views.admin_result, name='admin-result'),

    # for jquery

    path('get_questions', views.get_questions, name='get_questions'),
    path('submit_response', views.submit_response, name='submit_response'),
    path('get_questions_along_with_responses_for_evaluation', views.get_questions_along_with_responses_for_evaluation, name='get_questions_for_eval'),
    path('evaluate_response', views.evaluate_response, name='evaluate_response'),
]