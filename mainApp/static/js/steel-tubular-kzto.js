let paramsCount = 5;


document.body.addEventListener('focus', (event) => {
    let target = event.target;
    let manufacturer = document.getElementById('radiator-manufacturer').value;
    let appliance = document.getElementById('radiator-appliance-type').value;
    let length = Number.parseInt(document.getElementById('radiator-length').value);
    let mountingSize = Number.parseInt(document.getElementById('radiator-mounting-size').value);
    let connection = document.getElementById('radiator-connection').value;
    let applianceUnit = document.getElementById('radiator-appliance-type').dataset.unit;
    let lengthUnit = document.getElementById('radiator-length').dataset.unit;
    let mountingSizeUnit = document.getElementById('radiator-mounting-size').dataset.unit;
    let connectionUnit = document.getElementById('radiator-connection').dataset.unit;
    let currentOptions = [manufacturer, appliance, length, mountingSize, connection];


    if (target.id === 'radiator-appliance-type') {
       postOptions(
           currentOptions,
           fillEmptyParameters([manufacturer], paramsCount),
           'appliance-types-list',
           'appliance-type-item',
           applianceUnit
     );
    }
    if (target.id === 'radiator-length') {
       postOptions(
           currentOptions,
           fillEmptyParameters([manufacturer, appliance], paramsCount),
           'lengths-list',
           'length-item',
           lengthUnit
     );
    }
    if (target.id === 'radiator-mounting-size') {
       postOptions(
           currentOptions,
           fillEmptyParameters([manufacturer, appliance, length], paramsCount),
           'mounting-sizes-list',
           'mounting-size-item',
           mountingSizeUnit
     );
    }

    if (target.id === 'radiator-connection') {
       postOptions(
           currentOptions,
           fillEmptyParameters([manufacturer, appliance, length, mountingSize], paramsCount),
           'connections-list',
           'connection-item',
           connectionUnit
     );
    }
}, true);

document.body.addEventListener('click', (event) => {
    let target = event.target;
    let manufacturer = document.getElementById('radiator-manufacturer').value;
    let appliance = document.getElementById('radiator-appliance-type').value;
    let length = Number.parseInt(document.getElementById('radiator-length').value);
    let mountingSize = Number.parseInt(document.getElementById('radiator-mounting-size').value);
    let connection = document.getElementById('radiator-connection').value;
    if(target.id === 'manufacturer-item') {
        if(manufacturer !== "KZTO"){
            let path = window.location.href.split('/');
            console.log(path);
            path.splice(path.length -1, 1);
            path = path.join('/');
            location.href = path

        }else {
            postRadiator(
                fillEmptyParameters([manufacturer], paramsCount)
            );
        }
    }
    if(target.id === 'appliance-type-item') {
        postRadiator(
            fillEmptyParameters([manufacturer, appliance], paramsCount)
        );
    }
    if(target.id === 'length-item') {
        postRadiator(
            fillEmptyParameters([manufacturer, appliance, length], paramsCount)
        );
    }
    if(target.id === 'mounting-size-item') {
        postRadiator(
            fillEmptyParameters([manufacturer, appliance, length, mountingSize], paramsCount)
        );
    }
    if(target.id === 'connection-item') {
        postRadiator(
            fillEmptyParameters([manufacturer, appliance, length, mountingSize, connection], paramsCount)
        );
    }
});




