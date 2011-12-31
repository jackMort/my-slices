from django.test import TestCase
from django.contrib.auth.models import User

from slices.core.models import Slice, Vote


class SlicesTest( TestCase ):

    def setUp( self ):
        self.u1 = User.objects.create_user( "user1", "user1@user.com", "user" )
        self.u2 = User.objects.create_user( "user2", "user2@user.com", "user" )
        self.u3 = User.objects.create_user( "user3", "user3@user.com", "user" )

        self.s1 = Slice.objects.create( user=self.u1 )
        self.s2 = Slice.objects.create( user=self.u2 )

    def tearsDowm( self ):
        User.objects.all().delete()
        Slice.objects.all().delete()

    def test_votes( self ):
        self.assertEqual( self.s1.votes, 0 )
        self.assertEqual( self.s1.votes_sum, 0 )

        v1 = Vote.objects.create( user=self.u1, slice=self.s1, type=Vote.TYPE_PLUS )
        v2 = Vote.objects.create( user=self.u2, slice=self.s1, type=Vote.TYPE_PLUS )
        v3 = Vote.objects.create( user=self.u3, slice=self.s1, type=Vote.TYPE_MINUS )

        self.assertEqual( self.s1.votes, 3 )
        self.assertEqual( self.s1.votes_sum, 1 )
    
        v1.delete()

        self.assertEqual( self.s1.votes, 2 )
        self.assertEqual( self.s1.votes_sum, 0 )
        
        v2.delete()

        self.assertEqual( self.s1.votes, 1 )
        self.assertEqual( self.s1.votes_sum, -1 )
        
    


