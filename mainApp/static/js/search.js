document.body.addEventListener('focus', (event) => {
    if(event.target.id === 'search-input'){
        document.querySelector('#search-results').style.display = 'block';

    }

}, true);

document.body.addEventListener('input', (event) => {

    if(event.target.id === 'search-input'){
        let xhr = new XMLHttpRequest();
        let searchData = new FormData();

        xhr.open("POST",  window.location.protocol + '//' + window.location.host + '/catalog/main-search');
        searchData.append("search_string", document.getElementById('search-input').value);

        xhr.send(searchData);

        xhr.onload = () => (document.getElementById('search-results').innerHTML = xhr.responseText);
    }


}, true);

document.body.addEventListener('blur', (event) => {

    if(event.target.id === 'search-input'){
        document.querySelector('#search-results').style.display = 'none';
    }

}, true);