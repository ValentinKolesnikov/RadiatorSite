// $('#color').click(function(){
//   $('.extended-selection').show();
//   $('body').css('overflow', 'hidden')
// });
//
// $('.extended-selection__mask').click(function(){
//   $('.extended-selection').hide();
//   $('body').css('overflow', 'scroll')
//   $('body').css('overflow-x', 'hidden')
// });
//
// $('.extended-selection__list').click(function(event){
//   var target = event.target;
//   var colorBlock = document.getElementsByClassName('radiator__selected-color')[0];
//   console.log(target);
//   if(target.parentElement.className == "extended-selection__item"){
//     document.getElementById('color').innerHTML = target.parentElement.lastChild.previousElementSibling.innerHTML;
//     colorBlock.innerHTML = target.parentElement.innerHTML;
//     colorBlock.firstChild.className = '';
//     colorBlock.firstChild.nextSibling.className = 'radiator__selected-color-block';
//     colorBlock.lastChild.previousSibling.className = 'radiator__selected-color-name';
//
//     $('.extended-selection').hide();
//     $('body').css('overflow', 'scroll')
//     $('body').css('overflow-x', 'hidden')
//
//   }
//   // document.getElementById('color').innerHTML = target
// });
//
// $('#conection-type').click(function(){
//   $('.extended-selection-con').show();
//   $('body').css('overflow', 'hidden')
// });
//
// $('.extended-selection-con__mask').click(function(){
//   $('.extended-selection-con').hide();
//   $('body').css('overflow', 'scroll')
//   $('body').css('overflow-x', 'hidden')
// });
//
// $('.extended-selection-con__list').click(function(event){
//   var target = event.target;
//   var colorBlock = document.getElementsByClassName('radiator__selected-connection')[0];
//   console.log(target);
//   if(target.parentElement.className == "extended-selection-con__item"){
//     document.getElementById('conection-type').innerHTML = target.parentElement.lastChild.previousElementSibling.innerHTML;
//     colorBlock.innerHTML = target.parentElement.innerHTML;
//     colorBlock.firstChild.className = '';
//     colorBlock.firstChild.nextSibling.className = 'radiator__selected-connection-block';
//     colorBlock.lastChild.previousSibling.className = 'radiator__selected-connection-name';
//
//     $('.extended-selection-con').hide();
//     $('body').css('overflow', 'scroll')
//     $('body').css('overflow-x', 'hidden')
//
//   }
//   // document.getElementById('color').innerHTML = target
// });
//
//
// // document.body.onchange = function (event) {
// //   console.log(event.target.id);
// //   if(event.target.id == 'search-input'){
// //       document.getElementById('search-input').style.display = 'block'
// //   }
// // };
// //
// // $('.search-block__search').on("blur", function(){
// //   $('.results').css('display', "none")
// // });
//
