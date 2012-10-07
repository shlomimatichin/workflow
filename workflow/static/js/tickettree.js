function ticketTree( selector, options ) {
	this._options = { ticketAsRoot: undefined };
	$.extend( this._options, options );
	this._contextMenu = function( node ) {
		if ( ! node.attr( 'data-ticket' ) )
			return;
		var result =  {	'viewTicket' : {
							'label': 'View Ticket',
							'action': function( obj ) {
								document.location.href = "viewTicket?ticket=" + node.attr( 'data-ticket' );
					}, }, };
		if ( node.parent().parent().attr( 'data-ticket' ) )
			result.remove = {	'label': 'Remove From Parent',
								'action': function( obj ) {
									$.ajax( {
										'url': 'setRelation',
										'data' : {	'ticket': node.parent().parent().attr( 'data-ticket' ),
													'relatedTo': node.attr( 'data-ticket' ),
													'name': 'Not Parent Of' },
										'success' : $.proxy( function() {
											this.refresh( node.parent().parent() ); }, this ),
										'error' : $.proxy( function() {
											messageBox( 'Error', 'Unable to create relation' );
											this.refresh( node.parent().parent() ); }, this ), } );
							}, };
		return result;
	}

	this._checkMove = function( data ) {
		var dragged = data.o;
		var targetParent = data.np;
		if ( ! dragged.attr( 'data-ticket' ) )
			return false;
		if ( ! targetParent.attr( 'data-ticket' ) )
			return false;
		if ( targetParent.attr( 'data-ticket' ) == dragged.attr( 'data-ticket' ) )
			return false;
		var previousParentIDs = dragged.attr( 'data-parents' ).split( " " );
		if ( $.inArray( targetParent.attr( 'data-ticket' ), previousParentIDs ) != -1 )
			return false;
		return true;
	}

	this._nodeMoved = function( event, data ) {
		$.ajax( {	'url': 'setRelation',
					'data' : {	'ticket': data.rslt.np.attr( 'data-ticket' ),
								'relatedTo':data.rslt.o.attr( 'data-ticket' ),
								'name': 'Parent Of' },
					'success' : function() { data.rslt.ot.refresh( data.rslt.np ); },
					'error' : function() { messageBox( 'Error', 'Unable to create relation' );
											data.rslt.ot.refresh( data.rslt.np ); }, } );
	}

	var rootData;
	if ( this._options.ticketAsRoot ) {
		var ticket = this._options.ticketAsRoot;
		rootData = {	'data' : ticket.title,
						'attr' : { 'data-path' : '/Ticket/' + ticket.id, 'id': '_Ticket_' + ticket.id },
						'state' : 'closed' };
	} else
		rootData = {	"data" : "By Category",
						"attr" : { 'data-path' : '/By Category', 'id': '_By_Category' },
						"state" : "closed" };
	$(selector).jstree({
			"plugins" : ["themes","json_data","ui","hotkeys","contextmenu","cookies","crrm","dnd"],
			"themes" : { "theme" : "default", "icons" : false },
			"json_data" : {
				"data" : [ rootData, ],
				"ajax" : {	"url" : "/ticket/ticketTree",
							"data": function( node ) {
								return { 'path': node.attr( 'data-path' ) };
			} } },
			"contextmenu": { "items": this._contextMenuItems },
			"crrm": {
				'move': {	'always_copy': true,
							'open_onmove': true,
							'check_move': this._checkMove },
			},
			"dnd": { "drop_target": false, "drag_target": false },
	}).bind("move_node.jstree", this._nodeMoved );
}
