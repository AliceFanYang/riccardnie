$(document).ready(configure_events);


function configure_events() {
  $('.present_button').click(present_button_clicked);
}

function present_button_clicked(e) {
  var present_content_to_display = $(e.currentTarget.parentElement).find('.present_content')[0];
  var present_content = $(present_content_to_display).clone().addClass('display')[0];
  $(present_content).css('height', '50vh');
  var content = present_content.outerHTML;
  vex.open({
    content: content,
    contentCSS: {height:'50vh',
                padding: '0px 0px 0px 0px',}
  });
}
