function addBlankTargetForLinks() {
  $('a[href]').each(function(){
    $(this).attr('target', '_blank');
  });
}

$(document).ready(function(event) {
  addBlankTargetForLinks();
});