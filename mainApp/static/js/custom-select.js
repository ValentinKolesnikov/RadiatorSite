function showList(button) {
    let all_lists = document.getElementsByClassName('custom-select__list');
    if (all_lists) {
        for (let i = 0; i < all_lists.length; i++)
            all_lists[i].style.display = 'none';
    }

    let list = button.parentElement.childNodes[3];
    list.style.display = 'block';
}


function changeValue(target) {
    let button = target.parentElement.parentElement.childNodes[1];
    let list = target.parentElement.parentElement.childNodes[3];
    button.value = target.dataset.value;
    button.innerHTML = target.dataset.value + ' ' + button.dataset.unit;

    list.style.display = 'none';


}

