from django.contrib import admin
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
admin.autodiscover()
from views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    ('^$', base_redirect),
    ('^main/$', main_page),
    ('^account_reg/$', account_reg),
    ('^create_account/$', create_account),
    ('^account/$', account_access),
    ('^batch_test_upload/$', batch_test_upload),
    url('^batch_test_upload/$', batch_test_upload, name='batch_test_upload'),
    url('^batch_test_upload_final/$', batch_test_upload_final,
        name='batch_test_upload_final'),
    ('^new_model/$', model_regform),
    ('^model_created/$', model_created),
    ('^model_menu/$', model_access),
    (r'^admin/$', include(admin.site.urls)),
    ('^admin_login/$', admin_login),
    ('^admin_account/$', admin_account),
    ('^admin_cases/$', testcase_admin),
    ('^new_testcase/$', Casereg),
    ('^new_test/$', newtest),
    ('^create_test/$', create_test),
    ('^test_instructions/$', tst_instructions),
    ('^test_active/$', active_test),
    # ('^regen_test/$', regen_test),
    ('^upload_file/$', load_image),
    ('^Rate_Test/$', Rate),
    ('^confirm_grayscale/$', confirm_grayscale),
    ('^denygrayscale_confirm/$', denygrayscale_confirm),
    ('^acceptgrayscale_confirm/$', acceptgrayscale_confirm),
    ('^submissionreview/$', submissionreview),
    ('^nonactive_test/$', setcompletedtest),
    ('^Nonactive_test/$', nonactivetest),
    ('^Leader_model/$', Leader_model),
    ('^switchboard/$', switchboard),
    ('^model_to_test_switch/$', model_to_test_switch),
    ('^switchboard_totest/$', switchboard_totest),
    ('^case_info/$', testcaseshow),
    ('^return_leader/$', return_leader),
    ('^completedtest_info/$', completedtest_info),
    ('^case_ref/$', case_ref),
    ('^caseref_return/$', caseref_return),
    ('^Account_Profile/$', Account_Profile),
    ('^returnfrom_profile/$', returnfrom_profile),
    ('^case_hyperin/$', case_hyperin),
    ('^upload_casefile/$', upload_casefile),
    ('^exportcaselibrary/$', export_case_library),
    ('^Manage_Account/$', Manage_Account),
    ('^edit_user/$', edit_user),
    ('^edit_user_run/$', edit_user_run),
    ('^edit_inst/$', edit_inst),
    ('^edit_inst_run/$', edit_inst_run),
    ('^edit_pw/$', edit_pw),
    ('^edit_pw_run/$', edit_pw_run),
    ('^uploadprofpic/$', uploadprofpic),
    ('^accountregcomplete/$', accountregcomplete),
    ('^confirm_prof_pic/$', confirm_prof_pic),
    ('^denyprofpic_confirm/$', denyprofpic_confirm),
    ('^confirmprofpic_confirm/$', confirmprofpic_confirm),
    ('^edit_picture/$', edit_picture),
    ('^remove_profpic/$', remove_profpic),
    ('^alterprofpic/$', alterprofpic),
    ('^change_accountpic/$', change_accountpic),
    ('^traffic/$', traffic),
    ('^PasswordReset/$', password_reset),
    ('^CollectingData/$', collecting_data),
    ('^delete_account/$', delete_account),
    ('^deleteaccount_confirm/$', deleteaccount_confirm),
    ('^terminate_accounts/$', terminate_accounts),
    ('^view_username_admin/$', view_username_admin),
    ('^delaccountlink/$', delaccountlink),
    ('^adminterminate_account/$', adminterminate_account),
    ('^delete_model/$', delete_model),
    ('^deletemodel_confirm/$', deletemodel_confirm),
    ('^help/$', help),
    ('^help_how_alter_account/$', help_how_alter_account),
    ('^model_to_Scenario_switch/$', model_to_Scenario_switch),
    ('^switchboard_toscenario/$', switchboard_toscenario),
    ('^test_to_Scenario_switch/$', test_to_Scenario_switch),
    ('^test_to_test_switch/$', test_to_test_switch),
    ('^scenario_to_test_switch/$', scenario_to_test_switch),
    ('^scenario_to_scenario_switch/$', scenario_to_scenario_switch),
    ('^hyper_leaderboard/$', hyper_leaderboard),
    ('^password_reset/$', password_reset),
    ('^password_email/$', password_email),
    ('^CollectingData/$', collecting_data),
    ('^model_inst_sort/$', model_inst_sort),
    ('^model_name_sort/$', model_name_sort),
    ('^model_rtg_sort/$', model_rtg_sort),
    ('^model_tstscomp_sort/$', model_tstscomp_sort),
    ('^test_inst_sort/$', test_inst_sort),
    ('^test_modelname_sort/$', test_modelname_sort),
    ('^test_name_sort/$', test_name_sort),
    ('^test_rating_sort/$', test_rating_sort),
    ('^cat_inst_sort/$', cat_inst_sort),
    ('^cat_modelname_sort/$', cat_modelname_sort),
    ('^catrating_sort/$', catrating_sort),
    ('^catcompleted_sort/$', catcompleted_sort),
    ('^model_edit_info/$', model_edit_info),
    ('^model_change_info/$', model_change_info),
    ('^model_change_info/$', model_change_info),
    ('^model_Profile/$', model_Profile),
    ('^metric_description/$', metric_description),
    ('^metric_description_nonactive/$', metric_description_nonactive),
    ('^metric_description_submissionreview/$', metric_description_submissionreview),
    ('^reg_conditions/$', reg_conditions),
    ('^DownloadParam/$', download_param),
    ('^UploadLayers/$', upload_layers),
    ('^upload_Layerfile/$', upload_Layerfile),
    ('^DownloadLayers/$', DownloadLayers),
    ('^delete_Layers/$', delete_Layers),
    ('^DownloadLayersadmin/$', DownloadLayersadmin),
    ('^casetypeselect/$', casetypeselect),
    ('^NextSequentialTestSwitch/$', next_sequential_test_switch),
    ('^TesttypeSwitch/$', TesttypeSwitch),
    ('^TestNameSwitch/$', TestNameSwitch),
    (r'^robots\.txt$',
        lambda r: HttpResponse("User-agent: *\nDisallow: /",
                               mimetype="text/plain")),

    # Examples:
    # url(r'^$', 'MapRateWeb.views.home', name='home'),
    # url(r'^MapRateWeb/', include('MapRateWeb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
