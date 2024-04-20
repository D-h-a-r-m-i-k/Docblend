from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,re_path  
from .views import convert_images,pdf_collector_view,image_counter,pdf_counter,index,rename_images_view,start,add_logo_view,download_pdf,Requerments,to_do_delete,mark_task_completed


urlpatterns = [
    path('', start, name='start'),
    path('home/', index, name='index'),
    path('requerments/',Requerments,name='requerments'),
    path('images_to_PDFs', convert_images, name='convert_images'),
    path('pdf_collector/', pdf_collector_view, name='pdf_collector'),
    path('image_counter/', image_counter, name='image_counter'),
    path('pdf_page_counter/', pdf_counter, name='pdf_counter'),
    path('rename_images_view/', rename_images_view, name='rename_images_view'),
    path('add_logo/', add_logo_view, name='add_logo'),
    re_path(r'^download-pdf/(?P<path>.+)$', download_pdf, name='download_pdf'),
    path("delet-to-do/<int:to_do_id>",to_do_delete,name="to_do_delete"),
     path('mark-task-completed/', mark_task_completed, name='mark_task_completed'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



