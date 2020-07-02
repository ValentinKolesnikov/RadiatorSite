function removeItem(btn) {
    let xhr = new XMLHttpRequest();
    let productData = new FormData();

    let url = window.location.protocol + '//' + window.location.host + btn.dataset.removeUrl;

    xhr.open("POST", url);
    productData.append('id', btn.dataset.id);

    xhr.send(productData);

    xhr.onload = () => (document.body.innerHTML = xhr.responseText);
}

function changeQuantity(btn){

}

function removeQuantity(btn) {
    let xhr = new XMLHttpRequest();
    let productData = new FormData();

    let url = window.location.protocol + '//' + window.location.host + btn.dataset.changeQuantityUrl;

    xhr.open("POST", url);
    productData.append('id', btn.parentElement.parentElement.parentElement.id);
    productData.append('remove', true);

    xhr.send(productData);

    xhr.onload = () => (document.body.innerHTML = xhr.responseText);
}

function addQuantity(btn) {
    let xhr = new XMLHttpRequest();
    let productData = new FormData();

    let url = window.location.protocol + '//' + window.location.host + btn.dataset.changeQuantityUrl;

    xhr.open("POST", url);
    productData.append('id', btn.parentElement.parentElement.parentElement.id);
    productData.append('add', true);


    xhr.send(productData);

    xhr.onload = () => (document.body.innerHTML = xhr.responseText);
}