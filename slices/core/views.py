from django.views.generic.list import ListView

from slices.core.models import Slice

class SlicesListView( ListView ):
    template_name = "slices/list.html"
    context_object_name = 'slices'
    page_size = 50

    def get( self, *args, **kwargs ):
        self.t = self.request.GET.get( 't', None )
        return super( SlicesListView, self ).get( *args, **kwargs )

    def get_queryset( self ):
        qs = Slice.objects.all()
        if self.t:
            qs = qs.filter( type_cls= 'slice%s' % self.t )
        return qs

    def get_context_data( self, *args, **kwargs ):
        context = super( SlicesListView, self ).get_context_data( *args, **kwargs )
        context.update({ 't': self.t })
        return context


list = SlicesListView.as_view();
