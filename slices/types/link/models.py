from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from slices.types.link.utils import TagParser
from slices.core.models import Image, AbstractSlice

class SliceLink( AbstractSlice ):
    url = models.URLField( _( "url" ) )

    title = models.CharField( _( "title" ), max_length=250, blank=True, null=True )
    image = models.ForeignKey( Image, verbose_name = _( "image" ), blank=True, null=True )
    description = models.TextField( _( "text" ), blank=True, null=True )
    
    is_parsed = models.BooleanField( _( "is parsed" ), default=False )


    def save( self, *args, **kwargs ):
        super( SliceLink, self ).save( *args, **kwargs )
        if not self.is_parsed:
            parser = TagParser()
            metadata = parser.parse( self.url )
            print metadata

            self.title = metadata.get( 'title' )
            self.description = metadata.get( 'description' )
            image = metadata.get( 'image' )
            if image:
                print "saving image: %s " % image
                self.image = Image.objects.create( image_url=image, user=self.user )

            self.is_parsed = True
            self.save()

admin.site.register( SliceLink )
