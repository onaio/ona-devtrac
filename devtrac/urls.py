from django.conf import settings
from django.conf.urls import patterns, include, url, static
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from devtrac.main import views

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'devtrac.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^submission$', views.SubmissionPostView.as_view(),
        name='submission'),

    url(r'^admin/', include(admin.site.urls)),
) + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
