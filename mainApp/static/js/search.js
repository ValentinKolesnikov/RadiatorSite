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
         document.getElementById('search-results').innerHTML = '<div class="cssload-container" id="loading">\n' +
                    '                    <div class="cssload-speeding-wheel"></div>\n' +
                    '                </div>';
        document.getElementById('loading').style.display = 'block';
        document.getElementById('search-results').style.display = 'block';

        xhr.send(searchData);

        xhr.onload = () => {
            document.getElementById('loading').style.display = 'none';
            if (xhr.responseText) {
                document.getElementById('search-results').innerHTML = xhr.responseText;
            }
            else{

            }
            if(event.target.value === ''){
                document.getElementById('search-results').innerHTML = '<div class="cssload-container" id="loading">\n' +
                    '                    <div class="cssload-speeding-wheel"></div>\n' +
                    '                </div>';
            }
        };


    }


}, true);

document.body.addEventListener('click', (event) => {
    console.log(event.target.id);
    if(event.target.id !== 'search-results' && event.target.id !== 'search-input'){
        document.querySelector('#search-results').style.display = 'none';
    }

}, true);