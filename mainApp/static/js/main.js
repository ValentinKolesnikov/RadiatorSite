function add_to_cart() {
    let xhr = new XMLHttpRequest();
    let productData = new FormData();
    let info = document.getElementById('item-info');

    let url = window.location.protocol + '//' + window.location.host + info.dataset.url;
    console.log(info.dataset.id);
    console.log(info.dataset.type);
    xhr.open("POST", url);
    productData.append('id', info.dataset.id);
    productData.append('type', info.dataset.type);

    xhr.send(productData);

    document.getElementById('success-cart').style.display = 'flex';
    document.getElementById('mask').style.display = 'block';

}

function closeSuccessCart() {
    document.getElementById('success-cart').style.display = 'none';
    document.getElementById('mask').style.display = 'none';
}