
$(".comp-parts__name").text(function(i, text) {

    if (text.length >= 70) {
      text = text.substring(0, 70);
      var lastIndex = text.lastIndexOf(" ");
      text = text.substring(0, lastIndex) + '...';
    }
    
    $(this).text(text);
    
  });

$(".catalog__item-descr").text(function(i, text) {

  if (text.length >= 90) {
    text = text.substring(0, 90);
    var lastIndex = text.lastIndexOf(" ");
    text = text.substring(0, lastIndex) + '...';
  }
  
  $(this).text(text);
  
});