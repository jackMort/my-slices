from django.views.generic.list import ListView

from slices.core.models import Slice

class SlicesListView( ListView ):
    template_name = "slices/list.html"
    context_object_name = 'slices'
    page_size = 50

    def get_queryset( self ):
        return Slice.objects.all()

list = SlicesListView.as_view();
