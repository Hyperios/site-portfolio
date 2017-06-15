from django.views.decorators.cache import cache_page
from django.conf.urls import url
from . import views

app_name = 'shop'
urlpatterns = [
    url(r'^$', views.ShopView.as_view(), name='shop'),
    url(r'^photo/$', views.PhotoView.as_view(), name='photo'),
    url(r'^photo/(?P<pk>[0-9]+)/$', views.DetailPhotoView.as_view(), name='detail'),
    url(r'^photo/next/$', views.PhotoView.paginate_next, name='paginate_next'),
    url(r'^signup/$', views.register_user, name='register_user'),
    url(r'^register_success/$',
        views.PhotoView.register_success,
        name='register_success'),
    url(r'^confirm/(?P<activation_key>\w+)/$',
        views.register_confirm,
        name='register_confirm'),
    url(r'^login/$', views.PhotoView.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^password_reset/$', views.password_reload, name='password_restart'),
    url(r'^password_reset/done/$', views.success, name='password_reset_done'), 
    url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)\
        /(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', views.success_reset, name='password_reset_complete'),
    url(r'^contact/$', views.contact_view, name='contact'),
    url(r'^employer/$', views.employer_view, name='employer'),

]
