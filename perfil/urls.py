from django.conf.urls import patterns, include, url

urlpatterns = patterns('perfil.views', 
	url(r'^registrar/$', 'registrar'),
	url(r'^editar/$', 'editar'),
    url(r'^sucesso/(?P<username>\w+)$', 'sucesso'),
    url(r'^sucesso/', 'error'),
    url(r'^$', 'index'),
#    url(r'^(?P<usuario>\d+)/$', 'index'),
)

