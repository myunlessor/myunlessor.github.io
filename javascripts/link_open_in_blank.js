function addBlankTargetForLinks() {
  $('a[href^=http]').each(function(){
    $(this).attr('target', '_blank');
  });
}

$(document).ready(function(event) {
  addBlankTargetForLinks();
});