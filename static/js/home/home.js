let request = null;


function downloadFile(response) {
    console.log(response);
    //var a =  document.createElement('a');
    //a.style.display = 'none';
    //a.download = response
}


function initializeRow(tableId, html, code) {
    var table = document.getElementById(tableId);
    var tr = document.createElement('tr');
    tr.innerHTML = html;

    console.log(tr.getElementsByTagName('td'));

    table.appendChild(tr);
}


/**
 * Populates main table with
 * templates and their information.
 * @param {HTTP} response 
 */
function populateTable(response) {
    let templates = response;

    if (templates == null) {
        return;
    }
    
    $('#templates-list > tbody').html("");

    for (let template of templates) {
        let code = template['uuid'];
        let name = template['name'];
        let description = template['description'];

        var html = `\n<tr><td class="first-col">${name}</td>` +
        `<td class="second-col">${description}</td>`+
        `<td class="third-col"><form action="/edit-template"><input type="hidden" name="code" value=${code}><button>Edit</button></form></td>`
        + `<td class="fourth-col"><form action="/download-template" method="POST"><input type="hidden" name="code" value=${code}><button>Download</button></form></td></tr>`;
        initializeRow('templates-list', html, code);
    }
}


/**
 * Checks whether a response is
 * successful or not.
 * @param {HTTP} response 
 * @returns true if response is successful
 */
function checkValid(response) {
    console.log(response);

    if (response['success'] == true) {
        return true;
    } else {
        return false;
    }
}

/**
 * Function intended to begin
 * request for getting all
 * existing templates.
 */
function getTemplates() {
    let url = '/get-templates'

    if (request != null) {
        request.abort();
    }

    request = $.ajax(
        {
            type: 'POST',
            url: url,
            success: populateTable
        }
    )
}


/**
 * Sets up home with all user templates.
 */
function setup() {
    getTemplates();
}


window.onload = setup;