$(document).ready(function(){
  #("#form_submit").click(send_ajax_request);
});

//pass the info and smash it into a handler
function send_ajax_request(e){
  var form = $(e.currentTarget.parentElement);
  var title = form.find("#thankyou_post_title");
  var name = form.find("#");
}
