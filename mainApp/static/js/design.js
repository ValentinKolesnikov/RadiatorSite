let paramsCount = 3;


document.body.addEventListener('focus', (event) => {
    let target = event.target;
    let manufacturer = document.getElementById('radiator-manufacturer').value;
    let height = Number.parseInt(document.getElementById('radiator-height').value);
    let width = Number.parseInt(document.getElementById('radiator-width').value);
    let heightUnit = document.getElementById('radiator-height').dataset.unit;
    let widthUnit = document.getElementById('radiator-width').dataset.unit;
    let currentOptions = [manufacturer, height, width];


    if (target.id === 'radiator-height') {
       postOptions(
           currentOptions,
           fillEmptyParameters([manufacturer], paramsCount),
           'heights-list',
           'height-item',
           heightUnit
     );
    }
    if (target.id === 'radiator-width') {
       postOptions(
           currentOptions,
           fillEmptyParameters([manufacturer, height], paramsCount),
           'widths-list',
           'width-item',
           widthUnit
     );
    }

}, true);

document.body.addEventListener('click', (event) => {
    let target = event.target;
    let manufacturer = document.getElementById('radiator-manufacturer').value;
    let height = Number.parseInt(document.getElementById('radiator-height').value);
    let width = Number.parseInt(document.getElementById('radiator-width').value);

    if(target.id === 'manufacturer-item') {
        postRadiator(
            fillEmptyParameters([manufacturer], paramsCount)
        );
    }
    if(target.id === 'height-item') {
        postRadiator(
            fillEmptyParameters([manufacturer, height], paramsCount)
        );
    }
    if(target.id === 'width-item') {
        postRadiator(
            fillEmptyParameters([manufacturer, height, width], paramsCount)
        );
    }

});




