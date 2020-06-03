let paramsCount = 7;


document.body.addEventListener('focus', (event) => {
    let target = event.target;
    let side = document.getElementById('side-type').dataset.value;
    let lattice = document.getElementById('lattice-type').dataset.value;
    let manufacturer = document.getElementById('radiator-manufacturer').value;
    let model = document.getElementById('radiator-model').value;
    let height = Number.parseInt(document.getElementById('radiator-height').value);
    let width = Number.parseInt(document.getElementById('radiator-width').value);
    let connection = document.getElementById('radiator-connection').value;
    let heightUnit = document.getElementById('radiator-height').dataset.unit;
    let widthUnit = document.getElementById('radiator-width').dataset.unit;
    let connectionUnit = document.getElementById('radiator-connection').dataset.unit;
    let currentOptions = [manufacturer, model, height, width, connection];


    if (target.id === 'radiator-height') {
        postOptions(
            currentOptions,
            fillEmptyParameters([manufacturer, model, side, lattice], paramsCount),
            'heights-list',
            'height-item',
            heightUnit
        );
    }
    if (target.id === 'radiator-width') {
        postOptions(
            currentOptions,
            fillEmptyParameters([manufacturer, model, side, lattice, height], paramsCount),
            'widths-list',
            'width-item',
            widthUnit
        );
    }
    if (target.id === 'radiator-connection') {
        postOptions(
            currentOptions,
            fillEmptyParameters([manufacturer, model, side, lattice, height, width], paramsCount),
            'connections-list',
            'connection-item',
            connectionUnit
        );
    }
}, true);

document.body.addEventListener('click', (event) => {
    let target = event.target;
    let manufacturer = document.getElementById('radiator-manufacturer').value;
    let model = document.getElementById('radiator-model').value;
    let height = Number.parseInt(document.getElementById('radiator-height').value);
    let width = Number.parseInt(document.getElementById('radiator-width').value);
    // let length = Number.parseInt(document.getElementById('radiator-length').value);
    let connection = document.getElementById('radiator-connection').value;
    let side = document.getElementById('side-type').dataset.value;
    let lattice = document.getElementById('lattice-type').dataset.value;

    if (target.parentElement.id === 'side-type') {

        post_view_parameter_type(
            target.dataset.name,
            '',
            manufacturer,
            model
        );
    }
    if (target.parentElement.id === 'lattice-type') {

        post_view_parameter_type(
            side,
            target.dataset.name,
            manufacturer,
            model
        );
    }

    if (target.id === 'manufacturer-item') {
        postRadiator(
            fillEmptyParameters([manufacturer], paramsCount)
        );
    }
    if (target.id === 'model-item') {
        postRadiator(
            fillEmptyParameters([manufacturer, model], paramsCount)
        );
    }
    if (target.id === 'height-item') {
        postRadiator(
            fillEmptyParameters([manufacturer, model, side, lattice, height], paramsCount)
        );
    }
    if (target.id === 'width-item') {
        postRadiator(
            fillEmptyParameters([manufacturer, model, side, lattice, height, width], paramsCount)
        );
    }
    if (target.id === 'connection-item') {
        postRadiator(
            fillEmptyParameters([manufacturer, model, side, lattice, height, width, connection], paramsCount)
        );
    }
});

// document.body.addEventListener('focus', (event) => {
//     let target = event.target;
//
//     if (target.id === 'radiator-length') {
//        postOptions(
//            currentOptions,
//            fillEmptyParameters([manufacturer, model, side, lattice, height, width], paramsCount),
//            'connections-list',
//            'connection-item',
//            connectionUnit
//      );
//     }
// }, true);

function hideException(btn) {
    btn.parentElement.style.display = 'none';
}

function calculatePrice(lg) {
    let priceTag = document.getElementById('price');
    let priceUnit = parseFloat(priceTag.dataset.price.replace(',', '.'));
    let minLength = parseFloat(document.getElementById('radiator-length').min);
    let maxLength = parseFloat(document.getElementById('radiator-length').max);
    let stepLength = parseFloat(document.getElementById('radiator-length').step);
    let length = parseFloat(lg.value);

    if ((length - minLength) % stepLength !== 0 || length < minLength || length > maxLength) {
        document.getElementsByClassName('exception')[0].style.display = 'inline-block';
    } else {
        document.getElementsByClassName('exception')[0].style.display = 'none';
        let finalPrice = (priceUnit * length).toFixed(2);
        if (finalPrice)
            priceTag.innerHTML = finalPrice.toString().replace('.', ',') + ' р.';
        else
            priceTag.innerHTML = (priceUnit * minLength).toFixed(2).toString().replace('.', ',') + ' р.';
    }


}

