function postOptions(currentOptions=[], parameters=[], targetID, optionID, unit){
    let xhr = new XMLHttpRequest();
    let filterData = new FormData();
    xhr.open("POST", window.location.href);
    filterData.append('parameters', JSON.stringify(parameters));
    filterData.append('currentOptions', JSON.stringify(currentOptions));
    filterData.append('optionID', optionID);
    filterData.append('unit', unit);

    xhr.send(filterData);

    xhr.onload = () => {
        document.getElementById(targetID).innerHTML = xhr.responseText;
    };

}

function postRadiator(radiator=[]){
    let xhr = new XMLHttpRequest();
    let filterData = new FormData();
    xhr.open("POST", window.location.href);
    filterData.append('radiatorOptions', JSON.stringify(radiator));

    xhr.send(filterData);

    xhr.onload = () => (document.body.innerHTML = xhr.responseText);

}

function fillEmptyParameters(list=[], paramsCount){

    let finalList = [];
    for(let i = 0; i < paramsCount; i++)
        finalList.push(0);

    if(list)
        for(let i = 0; i < list.length; i++)
            finalList[i] = list[i];

    return finalList;
}