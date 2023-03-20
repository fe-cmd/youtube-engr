function DirectionsToggle(){
  var el = $('#dir-toggle');
  var dir_table = $('#dir-table')
  if (dir_table.attr("hidden") == "hidden") {
    dir_table.fadeIn()
    dir_table.removeAttr("hidden")
    el.html('hide <a href="javascript:void(0)" onclick="DirectionsToggle()">here')
  } else {
    dir_table.fadeOut()
    dir_table.attr("hidden", "hidden")
    el.html('click <a href="javascript:void(0)" onclick="DirectionsToggle()">here')
  }
}



function CopyText() {
  var text = document.getElementById('yourtext');
  text.select();
  document.execCommand('copy');
  alert('Text copied to clipboard!!!');
}

function status(clickedBtn) 
    {
      clickedBtn.value = "Copied to clipboard";
      clickedBtn.disabled = false;
      clickedBtn.style.color = 'white';
      clickedBtn.style.background = 'gray';

      //New Code
      copyToCliboard(clickedBtn.previousSibling);
    }
    function copyToCliboard(el) {
      if (document.body.createTextRange) {
          var range = document.body.createTextRange();
          range.moveToElementText(el);
          range.select();
      } else {
          var selection = window.getSelection();
          var range = document.createRange();
          range.selectNodeContents(el);
          selection.removeAllRanges();
          selection.addRange(range);
      }
      document.execCommand("copy");
      alert('Text copied to clipboard!!!');
      window.getSelection().removeAllRanges();
  }


