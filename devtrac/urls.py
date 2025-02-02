from django.conf import settings
from django.conf.urls import patterns, include, url, static

from django.contrib import admin
admin.autodiscover()

from devtrac.main import views

urlpatterns = patterns(
    '',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^fieldtrips\.(?P<format>(csv))$', views.FieldTripsView.as_view(),
        name='fieldtrips'),
    url(r'^places\.(?P<format>(csv))$', views.PlacesView.as_view(),
        name='places'),
    url(r'^submission$', views.SubmissionPostView.as_view(),
        name='submission'),

    url(r'^admin/', include(admin.site.urls)),
) + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
