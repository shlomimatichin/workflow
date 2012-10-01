var debug = true;

;(function($){
	$.traceInfo = function( message ) { 
		if ( debug ) {
			$._trace( message );
		}
	};
	$.traceError = function( message ) { 
		if ( debug ) {
			$._trace( message );
		}
	};
	$.listProperties = function( obj ) {
	   var propList = "";
	   for ( var propName in obj ) {
		  if( typeof( obj[ propName ] ) != "undefined" ) {
			 propList += ( propName + ", " );
		  }
	   }
	   return propList;
	};
})(jQuery);

String.prototype.format = function() {
  var args = arguments;
  return this.replace(/{(\d+)}/g, function(match, number) { 
    return typeof args[number] != 'undefined'
      ? args[number]
      : '{' + number + '}'
    ;
  });
};

function convertIntegerStringToHHMMSS( str ) {
    sec_numb    = parseInt( str );
    var hours   = Math.floor( sec_numb / 3600 );
    var minutes = Math.floor( ( sec_numb - ( hours * 3600 ) ) / 60 );
    var seconds = sec_numb - ( hours * 3600 ) - ( minutes * 60 );

    if ( hours   < 10 ) { hours   = "0"+hours; }
    if ( minutes < 10 ) { minutes = "0"+minutes; }
    if ( seconds < 10 ) { seconds = "0"+seconds; }
    var time = hours + ':' + minutes + ':' + seconds;
    return time;
}

function toFixed(value, precision) {
    var precision = precision || 0,
    neg = value < 0,
    power = Math.pow(10, precision),
    value = Math.round(value * power),
    integral = String((neg ? Math.ceil : Math.floor)(value / power)),
    fraction = String((neg ? -value : value) % power),
    padding = new Array(Math.max(precision - fraction.length, 0) + 1).join('0');

    return precision ? integral + '.' +  padding + fraction : integral;
}

function fakeSubmit( url, data, openANewWindow ) {
	if ( openANewWindow === undefined )
		openANewWindow = false;
	html = '<form id="fakesubmitid" style="display: none" name="fakeform" action="' + url + '" method="POST"';
	if ( openANewWindow )
		html += 'target="_blank"';
	html += '>';
	for ( var key in data )
		html += '<input type="text" name="' + key + '" value="' + data[ key ] + '"/>';
	html += '<input type="submit"/>';
	html += '</form>'
	$("body").append( html );
	document.fakeform.submit();
	$("#fakesubmitid").detach();
}

function is_int(value) { 
  if ( ( parseFloat(value) == parseInt( value ) ) && ! isNaN( value ) ) {
      return true;
  } else { 
      return false;
  } 
}
