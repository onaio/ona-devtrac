from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from devtrac.main import views

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'devtrac.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^submission$', views.SubmissionPostView.as_view()),

    url(r'^admin/', include(admin.site.urls)),
)
