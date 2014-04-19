$(function() {
	var loc_names = new Array();
	for(var i = 0; i < locations.length; i++)
		loc_names[i] = locations[i][1];

	$( "#event_location_name" ).autocomplete({
		source: loc_names
	});
});
