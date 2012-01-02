App = function() {
    return {
        MAX_PERPAGE: 10,
        init: function() {
            this.wall = jQuery( '.content' );

            this.wall.delegate( '.slice', 'mouseenter', this.slideMouseOver );
            this.wall.delegate( '.slice', 'mouseleave', this.slideMouseOut );

            this.masonry();
        },

        slideMouseOver: function() {
            $( '.header', $( this ) ).slideDown();
            console.log( 'slideMouseOver' )
        },
        slideMouseOut: function() {
            $( '.header', $( this ) ).slideUp();
            console.log( 'slideMouseOut' )
        },
        initializeScroll: function() {

            var parts = $( '.post', this.wall )
            var id = parts.length > 0 ? parts.last().attr( 'id' ) : 0
            var count = this.MAX_PERPAGE - parts.length
            jQuery( '#page_nav a' ).attr( "href", '/posts/fetch/' + id + '/'+ count )

            this.wall.infinitescroll({
                    navSelector  : '#page_nav',  // selector for the paged navigation 
                    nextSelector : '#page_nav a',  // selector for the NEXT link (to page 2)
                itemSelector : '.post',     // selector for all items you'll retrieve
                    loadingImg : 'img/loader.gif',
                donetext  : 'No more pages to load.',
                debug: true,
                errorCallback: function() { 
                    alert( "error callback" )
                    // fade out the error message after 2 seconds
                        //$('#infscr-loading').animate({opacity: .8},2000).fadeOut('normal');   
                }
                },
                // call masonry as a callback.
                    function( newElements ) { 
                    jQuery( this ).masonry({ appendedContent: jQuery( newElements ) }); 
                    jQuery( '.post:hidden' ).fadeIn()
                }
                );
        },
        masonry: function() {
            var masonry_options = {
                itemSelector: '.slice', 
                animate: true,
                // saveOptions: false,
                animateOptions: {
                    duration: 1000,
                    queue: false
                }
            };
            
            this.wall.masonry( masonry_options );

            jQuery( '.post:hidden' ).fadeIn()
        },
        bindActions: function( el ) {
            var self = this
            jQuery( '.post-close', el )
                .click( function() {
                    var post = $( this ).closest( '.post' )
                    self.closePost( post )
                })
        },
        closePost: function( el ) {
            var id = el.attr( 'id' )
            var self = this
            // ..
            jQuery.getJSON( '/readed/' + id, function( data ) {
                if ( data.success ) {
                    el.fadeOut( function() {
                        self.makeSelection( el.next() )
                        el.remove();
                        self.updateUnreadedCount( data.unreaded )
                        // fetch new parts
                        self.getParts()
                    })
                    // ..
                }
            })
        },
        /*getParts: function() {
            var self = this;
            var parts = $( '.post', this.wall )
            if( parts.length < this.MAX_PERPAGE ) {
                var id = parts.length > 0 ? parts.last().attr( 'id' ) : 0
                var count = this.MAX_PERPAGE - parts.length
                jQuery.get( '/posts/fetch/' + id + '/'+ count, function( data ) {
                        if( data.length > 10 ) {
                            var items = $( data )
                            items.css( 'position', 'absolute' );
                            self.bindActions( items )
                            self.wall.append( items )
                        }
                        self.masonry()
                    })
            }
        },*/
        makeSelection: function( post ) {
            jQuery( ".post.selected", this.wall ).removeClass( 'selected' )
            // ..
            this.selected = post;
            this.selected.addClass( 'selected' );
        },

        archive: function() {

        }
    }
}();

$(document).ready( function(){
    App.init.apply( App );
});
