from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', 'chat.views.index_view', name='index'),
    url(r'^conversation/(?P<pk>\d+)/$', 'chat.views.operator_conversation_view', name='operator-conversation'),
    url(r'^customer/$', 'chat.views.customer_index_view', name='customer-index'),
    url(r'^customer/conversation/(?P<pk>\d+)/$', 'chat.views.customer_conversation_view', name='customer-conversation'),

    url(r'^low_level/$', 'chat.views.low_level_view', name='low-level'),
    url(r'^admin/', include(admin.site.urls)),
]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
