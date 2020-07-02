let paramsCount = 5;


document.body.addEventListener('focus', (event) => {
    let target = event.target;
    let manufacturer = document.getElementById('radiator-manufacturer').value;
    let height = Number.parseInt(document.getElementById('radiator-height').value);
    let width = Number.parseInt(document.getElementById('radiator-width').value);
    let length = Number.parseInt(document.getElementById('radiator-length').value);
    let connection = document.getElementById('radiator-connection').value;
    let heightUnit = document.getElementById('radiator-height').dataset.unit;
    let widthUnit = document.getElementById('radiator-width').dataset.unit;
    let lengthUnit = document.getElementById('radiator-length').dataset.unit;
    let connectionUnit = document.getElementById('radiator-connection').dataset.unit;
    let currentOptions = [manufacturer, height, width, length, connection];


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
    if (target.id === 'radiator-length') {
       postOptions(
           currentOptions,
           fillEmptyParameters([manufacturer, height, width], paramsCount),
           'lengths-list',
           'length-item',
           lengthUnit
     );
    }

    if (target.id === 'radiator-connection') {
       postOptions(
           currentOptions,
           fillEmptyParameters([manufacturer, height, width, length], paramsCount),
           'connections-list',
           'connection-item',
           connectionUnit
     );
    }
}, true);

document.body.addEventListener('click', (event) => {
    let target = event.target;
    let manufacturer = document.getElementById('radiator-manufacturer').value;
    let height = Number.parseInt(document.getElementById('radiator-height').value);
    let width = Number.parseInt(document.getElementById('radiator-width').value);
    let length = Number.parseInt(document.getElementById('radiator-length').value);
    let connection = document.getElementById('radiator-connection').value;
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
    if(target.id === 'length-item') {
        postRadiator(
            fillEmptyParameters([manufacturer, height, width, length], paramsCount)
        );
    }
    if(target.id === 'connection-item') {
        postRadiator(
            fillEmptyParameters([manufacturer, height, width, length, connection], paramsCount)
        );
    }
});




