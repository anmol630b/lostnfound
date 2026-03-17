from django.urls import path
from . import views

urlpatterns = [
    path('',                    views.home_view,         name='home'),
    path('items/',              views.item_list_view,    name='item_list'),
    path('items/search/',       views.search_api,        name='search_api'),
    path('items/<int:pk>/',     views.item_detail_view,  name='item_detail'),
    path('items/post/',         views.post_item_view,    name='post_item'),
    path('items/post/lost/',    views.post_item_view,    {'item_type': 'lost'},  name='post_lost'),
    path('items/post/found/',   views.post_item_view,    {'item_type': 'found'}, name='post_found'),
    path('items/edit/<int:pk>/',    views.edit_item_view,    name='edit_item'),
    path('items/delete/<int:pk>/',  views.delete_item_view,  name='delete_item'),
    path('items/claim/<int:pk>/',   views.claim_item_view,   name='claim_item'),
    path('items/my-items/',         views.my_items_view,     name='my_items'),
    path('items/resolve/<int:pk>/', views.mark_resolved_view, name='mark_resolved'),
    path('items/report/pdf/',       views.pdf_report_view,   name='pdf_report'),
]
