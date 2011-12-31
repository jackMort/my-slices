import urllib
import mimetypes

from django.db import models
from django.contrib import admin
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.core.files.uploadedfile import SimpleUploadedFile

from taggit.managers import TaggableManager

class Slice( models.Model ):
    user = models.ForeignKey( User, verbose_name=_( "user" ) )
    added_at = models.DateTimeField( _( "added at" ), auto_now_add=True )
    type_cls = models.CharField( _( "type cls" ), max_length=100, blank=True, null=True )

    votes = models.IntegerField( _( "votes" ), default=0 )
    votes_sum = models.IntegerField( _( "votes sum" ), default=0 )

    tags = TaggableManager( blank=True )

    RENDER_FULL  = 1
    RENDER_SHORT = 2
    
    RENDERERS = {
        RENDER_FULL: 'full.html',
        RENDER_SHORT: 'short.html',
    }

    class Meta:
        verbose_name = _( "Slice" )
        verbose_name_plural = _( "Slices" )
        ordering = ( '-added_at', )

    @property
    def obj( self ):
        if self.type_cls:
            return getattr( self, self.type_cls, self )
        return self

    @property
    def all_votes( self ):
        return Vote.objects.filter( slice=self )

    @property
    def type_short_name( self ):
        return self.obj.__class__.__name__.lower().replace( 'slice', '' )

    def render( self, type=RENDER_FULL ):
        """
            renders slice as given type. 
            this method must be implemented in specified slice
        """
        from django.template.loader import select_template
        from django.template import Template, Context

        paths = [
            'slices/%s/%s' % ( self.type_short_name, self.RENDERERS.get( type ) )
        ]
        ctx = Context({
            'slice': self.obj
        })
        template = select_template( paths )
        return template.render( ctx )

    def save( self, *args, **kwargs ):
        self.type_cls = self.__class__.__name__.lower()
        super( Slice, self ).save( *args, **kwargs )

class AbstractSlice( Slice ):

    class Meta:
        abstract = True

    @property
    def tags( self ):
        # override to get tags from parent slice
        return Slice.objects.get( id=self.slice_ptr_id ).tags


class Vote( models.Model ):
    TYPE_PLUS  = 1
    TYPE_MINUS = -1

    TYPE_CHOICES = (
        ( TYPE_PLUS, _( 'plus' ) ),
        ( TYPE_MINUS, _( 'minus' ) ),
    )

    user = models.ForeignKey( User, verbose_name=_( "user" ) )
    slice = models.ForeignKey( Slice, verbose_name=_( "Slice" ) )
    type = models.IntegerField( _( "type" ), choices=TYPE_CHOICES, default=TYPE_PLUS )

    class Meta:
        verbose_name = _( "Vote" )
        verbose_name = _( "Votes" )
        unique_together = ( 'user', 'slice' )

    @classmethod
    def update_votes_cache( cls, sender, instance, *args, **kwargs ):
        try:
            slice = instance.slice
            votes = Vote.objects.filter( slice=slice ).aggregate( sum=Sum( 'type' ), count=Count( 'type' ) )
            slice.votes = votes['count']
            slice.votes_sum = votes['sum'] or 0
            slice.save()
        except Slice.DoesNotExist:
            pass # already removed, ignore

class Image( models.Model ):
    user = models.ForeignKey( User, verbose_name=_( "user" ) )
    image = models.ImageField( _( "image" ), null=True, blank=True, upload_to="uploads/images/" )
    image_url = models.URLField( _( "image url" ), null=True, blank=True )
    uploaded_at = models.DateTimeField( _( "uploaded at" ), auto_now_add=True )

    class Meta:
        verbose_name = _( 'Image' )
        verbose_name_plural = _( 'Images' )

    @property
    def url( self ):
        return self.image.url

    def get_thumbnail( self, **kwargs ):
        from easy_thumbnails.files import get_thumbnailer
        kwargs['size'] = kwargs.get( 'size', ( 100, 100 ) )
        kwargs['crop'] = kwargs.get( 'crop', 'smart' )
        kwargs['sharpen'] = kwargs.get( 'sharpen', True )
        kwargs['detail'] = kwargs.get( 'detail', True )
        return get_thumbnailer( self.image ).get_thumbnail( kwargs )

    def save( self, *args, **kwargs ):
        super( Image, self ).save( *args, **kwargs )
        if not self.image and self.image_url:
            filename, headers = urllib.urlretrieve( self.image_url.encode( 'utf-8' ) )
            type = headers.get( 'Content-Type' )
            if not type or not mimetypes.guess_all_extensions( type ):
                raise ValidationError( 'Broken image !' )
            self.image = SimpleUploadedFile( filename, open( filename ).read(), content_type=type )
            self.save()

# register admin sites
admin.site.register( Vote )
admin.site.register( Image )
admin.site.register( Slice )

# connect signals
post_save.connect( Vote.update_votes_cache, sender=Vote )
post_delete.connect( Vote.update_votes_cache, sender=Vote )

