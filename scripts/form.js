$(document).ready(function(){
  $("#form_submit").click(send_ajax_request);
});

function send_ajax_request(e){
  var form = $(e.currentTarget.parentElement);
  var post_title = form.find("#thankyou_post_title");
  var icon_img_link = form.find("#thankyou_icon_link");
  var message = form.find("#thankyou_message");
  var riccardo_img_link = form.find("#thankyou_ricc_link");
  var riccardo_caption = form.find("#thankyou_ricc_caption");
  var sidnie_img_link = form.find("#thankyou_sidn_link");
  var sidnie_caption = form.find("#thankyou_sidn_caption");
  //console.log("Just about to send ajax");
  $.ajax({
    type: "POST",
    method: "POST",
    url: "/save-post",
    data: {
      "post_title": post_title.val(),
      "icon_img_link": icon_img_link.val(),
      "message": message.val(),
      "riccardo_img_link": riccardo_img_link.val(),
      "riccardo_caption": riccardo_caption.val(),
      "sidnie_img_link": sidnie_img_link.val(),
      "sidnie_caption": sidnie_caption.val()
    }
  }).done(function(msg){
    console.log("added!");
    window.location.replace("/");
  });
}
