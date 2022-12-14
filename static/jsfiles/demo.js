
$(document).ready(function(){
  $("#hello1").hide();
  $("#hello2").hide();
  $("#hello3").hide();
  $("#one").click(function(){
    $("#hello1").toggle(100);
    $('#one').toggleClass('fa fa-toggle-off fa fa-toggle-on');

  });
  $("#two").click(function(){
    $("#hello2").toggle(100);
    $('#two').toggleClass('fa fa-toggle-off fa fa-toggle-on');
  });
   $("#three").click(function(){
    $("#hello3").toggle(100);
    $('#three').toggleClass('fa fa-toggle-off fa fa-toggle-on');
  });
});



//two


$(document).ready(function(){
  $("#hello1-one").hide();
  $("#hello2-two").hide();
  $("#hello3-three").hide();
  $("#one-one").click(function(){
    $("#hello1-one").toggle(100);
    $('#one-one').toggleClass('fa fa-toggle-off fa fa-toggle-on');

  });
  $("#two-two").click(function(){
    $("#hello2-two").toggle(100);
    $('#two-two').toggleClass('fa fa-toggle-off fa fa-toggle-on');
  });
   $("#three-three").click(function(){
    $("#hello3-three").toggle(100);
    $('#three-three').toggleClass('fa fa-toggle-off fa fa-toggle-on');
  });
});





