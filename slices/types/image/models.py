from django.db import models
from django.contrib import admin
from slices.core.models import Image, AbstractSlice
from django.utils.translation import gettext_lazy as _

class SliceImage( AbstractSlice ):
    image = models.ForeignKey( Image, verbose_name = _( "image" ) )

admin.site.register( SliceImage )
