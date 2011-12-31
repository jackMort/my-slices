from django.db import models
from django.contrib import admin
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, post_delete

from taggit.managers import TaggableManager

class Slice( models.Model ):
    user = models.ForeignKey( User, verbose_name=_( "user" ) )
    added_at = models.DateTimeField( _( "added at" ), auto_now_add=True )

    votes = models.IntegerField( _( "votes" ), default=0 )
    votes_sum = models.IntegerField( _( "votes sum" ), default=0 )

    @property
    def votes_all( self ):
        return Vote.objects.filter( slice=self )

    tags = TaggableManager()

    RENDER_FULL  = 1
    RENDER_SHORT = 2

    class Meta:
        verbose_name = _( "Slice" )
        verbose_name_plural = _( "Slices" )
        ordering = ( '-added_at', )

    def render( self, type=RENDER_FULL ):
        """
            renders slice as given type. 
            this method must be implemented in specified slice
        """
        raise NotImplemented

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
        slice = instance.slice
        votes = Vote.objects.filter( slice=slice ).aggregate( sum=Sum( 'type' ), count=Count( 'type' ) )
        slice.votes = votes['count']
        slice.votes_sum = votes['sum'] or 0
        slice.save()

# register admin sites
admin.site.register( Vote )
admin.site.register( Slice )

# connect signals
post_save.connect( Vote.update_votes_cache, sender=Vote )
post_delete.connect( Vote.update_votes_cache, sender=Vote )


