"use strict";

$('#update-status').on('click', () => {

$.get('/getuserpreferences.json', (response) => {
    $('#preferred-subtitle-default').value(response['audio']);
    $('#preferred-subtitle-default').text(response['audio']);
  });
});



jQuery( document ).ready(function() {

  jQuery('.opener h5').click(function() {
  jQuery(this).next('.hidden-div').toggle();
  jQuery(this).children('i.fas').toggle();
  })
  
});

 

jQuery( document ).ready(function() {

  jQuery('.opener h1').click(function() {
  jQuery(this).next('.hidden-div').toggle();
  jQuery(this).children('i.fas').toggle();
  })
  
});

 

