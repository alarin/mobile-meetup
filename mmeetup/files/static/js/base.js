$(function() {
   $('.agenda tr').mouseover(function(){
        $(this).find('.extra').show();
   });
   $('.agenda tr').mouseout(function(){
        $('.agenda .extra').hide();
   });
});