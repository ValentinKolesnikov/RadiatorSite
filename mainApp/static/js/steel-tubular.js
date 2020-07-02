let paramsCount = 5;


document.body.addEventListener('focus', (event) => {
    let target = event.target;
    let manufacturer = document.getElementById('radiator-manufacturer').value;
    let height = Number.parseInt(document.getElementById('radiator-height').value);
    let width = document.getElementById('radiator-width').value;
    let depth = Number.parseInt(document.getElementById('radiator-depth').value);
    let connection = document.getElementById('radiator-connection').value;
    let heightUnit = document.getElementById('radiator-height').dataset.unit;
    let widthUnit = document.getElementById('radiator-width').dataset.unit;
    let depthUnit = document.getElementById('radiator-depth').dataset.unit;
    let connectionUnit = document.getElementById('radiator-connection').dataset.unit;
    let currentOptions = [manufacturer, height, width, depth, connection];


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
    if (target.id === 'radiator-depth') {
       postOptions(
           currentOptions,
           fillEmptyParameters([manufacturer, height, width], paramsCount),
           'depths-list',
           'depth-item',
           depthUnit
     );
    }

    if (target.id === 'radiator-connection') {
       postOptions(
           currentOptions,
           fillEmptyParameters([manufacturer, height, width, depth], paramsCount),
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
    let width = document.getElementById('radiator-width').value;
    let depth = Number.parseInt(document.getElementById('radiator-depth').value);
    let connection = document.getElementById('radiator-connection').value;
    if(target.id === 'manufacturer-item') {
        if(manufacturer === "KZTO"){
            location.href = document.getElementById('radiator-manufacturer').dataset.kzto;
        }else {
            postRadiator(
                fillEmptyParameters([manufacturer], paramsCount)
            );
        }
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
    if(target.id === 'depth-item') {
        postRadiator(
            fillEmptyParameters([manufacturer, height, width, depth], paramsCount)
        );
    }
    if(target.id === 'distance-item') {
        postRadiator(
            fillEmptyParameters([manufacturer, height, width, depth, distance], paramsCount)
        );
    }
    if(target.id === 'connection-item') {
        postRadiator(
            fillEmptyParameters([manufacturer, height, width, depth, distance, connection], paramsCount)
        );
    }
});




