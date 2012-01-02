import urllib2
import urlparse
import BeautifulSoup

def get_base_url( url ):
    return urlparse.urlsplit( url ).netloc.replace( 'www.', '' )

class DemotywatoryPlProcessor:
    def __init__( self, parser ):
        self.parser = parser

    def match( self, url ):
       return get_base_url( url ) == 'demotywatory.pl'

    def process( self, metadata ):
        metadata['image'] = metadata.get( 'image' ).replace( '_120', '' )
        return metadata

class TagParser( object ):

    OG_TAGS = [
        'title', 'type', 'image', 'url', 'description', 'site_name', 'email', 'phone_number',
        'fax_number', 'latitude', 'longitude', 'street-address', 'locality', 'region', 'postal-code',
        'country-name', 'video', 'video:height', 'video:width', 'video:type', 'audio', 'audio:title',
        'audio:artist', 'audio:album', 'audio:type'
    ]

    PROCESSORS = [
        DemotywatoryPlProcessor,
    ]

    def parse( self, url, required_properties=[ 'title', 'url', 'description', 'image' ] ):
        self.content = urllib2.urlopen( url ).read()
        self.soup = BeautifulSoup.BeautifulSoup( self.content )

        metadata = self.parseOG()
        for property in required_properties:
            if not metadata.get( property ):
                metadata[property] = self.get_property( property )


        for cls in self.PROCESSORS:
            processor = cls( self )
            if processor.match( url ):
                metadata = processor.process( metadata )

        return metadata

    def parseOG( self ):
        metadata = {}
        for tag in self.OG_TAGS:
            og = self.soup.findAll( property='og:%s' % tag )
            if len( og ):
                 metadata[tag] = og[0]["content"]
        return metadata
    
    def get_property( self, property ):
        return ""
