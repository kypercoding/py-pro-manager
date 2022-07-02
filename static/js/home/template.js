let request = null;


/**
 * Alerts user of error given a
 * response from server.
 * @param {JSON} response
 */
function showError(response) {
    alert(response.responseJSON['error']);
}


/**
 * Delete the template.
 */
function deleteTemplate() {
    var code = document.getElementById('hidden-input').value;

    let url = "/delete-template";

    var data = {'code': code};

    if (request != null) {
        request.abort();
    }

    request = $.ajax(
        {
            url: url,
            type: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(data),
            success: returnHome
        }
    );
}


/**
 * Gets any JSON data passed by server
 * and fills in tables.
 */
function fillTables(response) {
    var data = response;
    var sep = data['sep'];

    for (var object in data['objects']) {
        var result = data['objects'][object].split(sep);

        if (result[0] == 'True') {
            result[0] = " checked";
        } else {
            result[0] = "";
        }

        var html = `<tr><td class="col-1"><button class="delete" ` + 
    `onclick="deleteRow(this)">Delete</button></td><td class="col-2">` +
    `<input type="text" placeholder="Type file or directory path" value="${result[1]}">` +
    `</td><td class="col-3"><input class="checkbox" type="checkbox" ${result[0]}></td></tr>\n`;
        initializeRow('objects-table', html, response);
    }
    
    for (var package in data['packages']) {
        var packageName = data['packages'][package];
        var html = `<tr><td class="p-col-1"><button class="delete" onclick="deleteRow(this)">` +
        `Delete</button></td><td class="p-col-2"><input placeholder="Type package" type="text" value=${packageName}></td></tr>\n`;
        initializeRow('packages-table', html, response);
    }

    var nameInput = document.getElementById('name-input');
    nameInput.value = data['name'];
    var descriptionInput = document.getElementById('description-input');
    descriptionInput.value = data['description'];
}


/**
 * Calls for JSON data to call
 * fillTables().
 * @param {String} code
 */
function getData(code) {
    let url = "/get-template";

    var codeData = {'code': code};

    request = $.ajax(
        {
            contentType: 'application/json',
            url: url,
            type: 'POST',
            data: JSON.stringify(codeData),
            success: fillTables
        }
    );
}


/**
 * Opens the packages tab.
 */
function openPackages() {
    var divObjects = document.getElementById('objects-container');
    var divPackages = document.getElementById('packages-container');
    var divInformation = document.getElementById('info-container');

    divObjects.style.display = "none";
    divPackages.style.display = "block";
    divInformation.style.display = 'none';
}

/**
 * Opens the objects tab.
 */
function openObjects() {
    var divObjects = document.getElementById('objects-container');
    var divPackages = document.getElementById('packages-container');
    var divInformation = document.getElementById('info-container');

    divObjects.style.display = "block";
    divPackages.style.display = "none";
    divInformation.style.display = 'none';
}

/**
 * Opens the information tab.
 */
function openInformation() {
    var divObjects = document.getElementById('objects-container');
    var divPackages = document.getElementById('packages-container');
    var divInformation = document.getElementById('info-container');

    divObjects.style.display = "none";
    divPackages.style.display = "none";
    divInformation.style.display = 'block';
}


/**
 * Initializes table row with
 * all the necessary event
 * handlers.
 * @param {Object} tableId
 * @param {String} html
 * @param {Object} object
 */
function initializeRow(tableId, html, object) {
    var table = document.getElementById(tableId);
    var tr = document.createElement('tr');
    tr.innerHTML = html;
    
    var inputTag = tr.getElementsByTagName('td')[1].firstChild;
    
    inputTag.addEventListener('keydown', e => {
        if (e.key == 'Backspace' || e.keyCode == 8) {
            deleteRow(e.target);
        }
        
        if (e.key == 'Enter' || e.keyCode == 13) {
            if (getCurrentTab() == "objects") {
                addObjectRow(e.target);
            } else if (getCurrentTab() == "packages") {
                addPackageRow(e.target);
            } else {
                return;
            }
        }
    });

    if (object instanceof HTMLButtonElement || object instanceof PointerEvent) {
        table.appendChild(tr);
    } else if (object instanceof HTMLInputElement) {
        table.insertBefore(tr, object.parentNode.parentNode);
    } else {
        table.appendChild(tr);
    }
}

/**
 * Obtains the current tab selected in
 * drop down menu.
 * @returns value of dropdown menu
 */
function getCurrentTab() {
    var value = document.getElementById('dropdown').value;

    return value;
}


/**
 * Add file/directory row to element.
 * @param {Object} object after which
 * to insert the new row. 
 */
function addObjectRow(object) {
    if (getCurrentTab() != "objects") {
        return;
    }

    var html = '<tr><td class="col-1"><button class="delete" ' + 
    'onclick="deleteRow(this)">Delete</button></td><td class="col-2">' +
    '<input type="text" placeholder="Type file or directory path">' +
    '</td><td class="col-3"><input class="checkbox" type="checkbox"></td></tr>';

    initializeRow('objects-table', html, object);
}

/**
 * Add package row to element. 
 */
function addPackageRow(object) {
    if (getCurrentTab() != "packages") {
        return;
    }

    var html = '<tr><td class="p-col-1"><button class="delete" onclick="deleteRow(this)">' +
    'Delete</button></td><td class="p-col-2"><input placeholder="Type package" type="text"></td></tr>';

    initializeRow('packages-table', html, object);
}

/**
 * Delete row.
 * @param {Object} o
 */
function deleteRow(o) {
    var td = o.parentNode;
    var tr = td.parentNode;

    if (o instanceof HTMLButtonElement || o instanceof PointerEvent) {
        tr.parentNode.removeChild(tr);
    } else {
        if (o.value == "") {
            tr.parentNode.removeChild(tr);
        }
    }
}

/**
 * Change tab to selected value.
 */
function change() {
    var selectBox = document.getElementById("dropdown");
    var selectedValue = selectBox.options[selectBox.selectedIndex].value;

    if (selectedValue == 'objects') {
        openObjects();
    } else if (selectedValue == 'packages') {
        openPackages();
    } else {
        openInformation();
    }
}


const getSizeInBytes = obj => {
    let str = null;
    if (typeof obj === 'string') {
      // If obj is a string, then use it
      str = obj;
    } else {
      // Else, make obj into a string
      str = JSON.stringify(obj);
    }
    // Get the length of the Uint8Array
    const bytes = new TextEncoder().encode(str).length;
    return bytes;
};


function logSizeInBytes(description, obj) {
    const bytes = getSizeInBytes(obj);
    console.log(`${description} is approximately ${bytes} B`);
}


/**
 * Sends row information to server to store
 * packages and files/directories.
 */
function sendInformation() {
    var objectRows = document.querySelector('#objects-table');
    var packageRows = document.querySelector('#packages-table');

    var name = document.getElementById('name-input').value;
    var description = document.getElementById('description-input').value;
    var code = document.getElementById('hidden-input').value;

    var check = true;

    var data = {'code': code, 'name': name, 'description': description, 'objects': [], 'packages': []};

    for (var object of objectRows.rows) {
        if (check) {
            check = false;
            continue;
        }

        var dict = {};

        dict['object'] = object.cells[1].firstChild.value;

        if (object.cells[2].firstChild.checked == true) {
            dict['is_file'] = "True";
        } else {
            dict['is_file'] = "False";
        }

        data['objects'].push(dict);
    }

    check = true;

    for (var package of packageRows.rows) {
        if (check) {
            check = false;
            continue;
        }

        data['packages'].push(package.cells[1].firstChild.value);
    }

    let url = '/save-template'

    if (request != null) {
        request.abort();
    }

    request = $.ajax(
        {
            type: 'POST',
            url: url,
            contentType: "application/json",
            dataType: 'json',
            data: JSON.stringify(data),
            success: returnHome,
            error: showError
        }
    );
}


/**
 * Return to home page.
 */
function returnHome() {
    if (request != null) {
        request.abort();
    }

    request = $.ajax(
        {
            type: 'GET',
            success: function(){
                window.location.href = "home";
            }
        }
    );
}


window.onload = function() {
    var selectBox = document.getElementById('dropdown');
    selectBox.addEventListener('change', change);
    
    var submitButton = document.getElementById('submit-button');
    submitButton.addEventListener('click', sendInformation);

    var deleteButton = document.getElementById('delete-button');
    deleteButton.addEventListener('click', deleteTemplate);

    var returnButton = document.getElementById('return-button');
    returnButton.addEventListener('click', returnHome);

    var objectsButton = document.getElementById('add-row');
    objectsButton.addEventListener('click', e => {
        var value = selectBox.value;
        if (value === "objects") {
            addObjectRow(e.target);
        } else {
            addPackageRow(e.target);
        }
    });
}
