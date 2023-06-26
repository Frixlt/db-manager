function setStatus(status) {
    var statusElement = document.getElementById('status');
    statusElement.innerHTML = status;
    statusElement.className = status;
  }
// функция отвечающая за отображение меню
function toggleMenu() {
    var menuBtn = document.querySelector('.menu-btn');
    var container = document.querySelector('.menu-container');
    var menuItems = document.querySelector('.menu-items');
    menuBtn.classList.toggle('active');
    container.classList.toggle('active');
    menuItems.classList.toggle('active');
}
// функция отвечающая за отображение инструментов
function toggleTools() {
    const toolsBtn = document.querySelector('.tools-btn');
    const containerTools = document.querySelector('.tools-container');
    toolsBtn.classList.toggle('active');
    containerTools.classList.toggle('active');
}
//функция отвечающая за переключение тем
function toggleTheme() {
    document.body.classList.toggle('dark');
}
//запоминание сотсояния ползунка перекключателя тем
window.addEventListener('DOMContentLoaded', function () {
    var themeSwitch = document.querySelector('.theme_switch_label input');
    // Восстановление состояния переключателя при загрузке страницы
    var theme = localStorage.getItem('theme');
    if (theme === 'dark') {
        themeSwitch.checked = true;
        document.body.classList.add('dark');
    }
    // Обработчик изменения состояния переключателя
    themeSwitch.addEventListener('change', function () {
        if (this.checked) {
            document.body.classList.add('dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.classList.remove('dark');
            localStorage.setItem('theme', 'light');
        }
    });
});
//функция отвечающая за изменения цвета вкладок
function changeTab(tabIndex) {
    var tabButtons = document.querySelectorAll('.menu-tab-button');
    for (var i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
    }
    var selectedTabButton = document.querySelector('#menu-tab-button-' + tabIndex);
    selectedTabButton.classList.add('active');

    var tabContents = document.querySelectorAll('.tab-content');
    for (var i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove('active');
    }
    var selectedTab = document.querySelector('#tab-content-' + tabIndex);
    selectedTab.classList.add('active');
}
// функция показывающая уведомления
function showNotification(title, text) {
    var popup = document.createElement('div');
    popup.className = 'popup';

    var closeButton = document.createElement('span');
    closeButton.className = 'close-btn';
    closeButton.innerText = 'X';
    closeButton.onclick = function () {
        popup.classList.remove('show');
        setTimeout(function () {
            popup.style.display = 'none';
        }, 500);
    };

    var heading = document.createElement('h3');
    heading.innerText = title;

    var content = document.createElement('p');
    content.innerText = text;

    popup.appendChild(closeButton);
    popup.appendChild(heading);
    popup.appendChild(content);

    document.body.appendChild(popup);

    setTimeout(function () {
        popup.classList.add('show');
    }, 0); // Выезд окна без задержки

    setTimeout(function () {
        popup.classList.remove('show');
        setTimeout(function () {
            popup.style.display = 'none';
        }, 500);
    }, 3000); // Закрытие окна

    // пример вызова
    // showNotification('Заголовок уведомления', 'Текст уведомления')
}
//функция отвечающая за изменение div в таблице
document.addEventListener('DOMContentLoaded', function () {
    var divs = document.querySelectorAll('td div');
    for (var i = 0; i < divs.length; i++) {
        divs[i].addEventListener('click', function () {
            this.classList.add('expanded');
        });
        divs[i].addEventListener('blur', function () {
            this.classList.remove('expanded');
        });
    }
});
// отправка на сервер
function sendData() {
    var rows = document.querySelectorAll('#general_base tbody tr');
    var data = [];

    rows.forEach(function (row) {
        var rowData = {};
        var cells = row.querySelectorAll('td:not(.button-cell) div');

        cells.forEach(function (cell, index) {
            var columnHeader = getColumnHeader(index);
            rowData[columnHeader] = cell.innerText;
        });

        data.push(rowData);
    });
    socket.emit('update', data)
}
function getColumnHeader(index) {
    var headers = Array.from(document.querySelectorAll('#general_base thead th')).map(function (header) {
        return header.innerText;
    });
    return headers[index];
}

function openNewWin(url) {
    myWin = open(url);
}

function getTitleNames(exim) {
    if (exim == true) {
        var windowTiles = document.getElementById('exportWindowTiles');
        var insertColums = document.getElementById('insertColums').checked;
        var limit_acaunts = document.getElementById('limit-accounts').value;
        var divider = document.getElementsByName('export-divider')[0].value;
    }
    else {
        var textarea = document.querySelector('.import .textarea-container textarea').value;
        var windowTiles = document.getElementById('importWindowTiles');
        var divider = document.getElementsByName('import-divider')[0].value;
    }
    if (divider == "") {
        divider = ":";
    }
    var movedTiles = windowTiles.getElementsByClassName('tile');
    var tileNames = [];
    for (var i = 0; i < movedTiles.length; i++) {
        var tileName = movedTiles[i].textContent;
        tileNames.push(tileName);
    }
    if (exim == true) {
        return ([divider, tileNames, limit_acaunts, insertColums])
    }
    else {
        return ([divider, tileNames, textarea])
    }
}

function ImportTiles() {
    var importedData = getTitleNames();
    var textarea = document.querySelector('.import .textarea-container textarea');
    textarea.value = importedData;
}

function drag(event) {
    event.dataTransfer.setData("text/plain", event.target.id);
    event.target.classList.add("dragging");
}

function importDrop(event) {
    event.preventDefault();
    var data = event.dataTransfer.getData("text/plain");
    var draggableTile = document.getElementById(data);
    var targetTile = event.target;
    if (targetTile.classList.contains("tile")) {
        var tempTile = document.createElement("div");
        draggableTile.parentNode.insertBefore(tempTile, draggableTile);
        targetTile.parentNode.insertBefore(draggableTile, targetTile);
        tempTile.parentNode.insertBefore(targetTile, tempTile);
        tempTile.parentNode.removeChild(tempTile);
        draggableTile.classList.remove("dragging");
    } else if (targetTile.classList.contains("tile-container")) {
        var importWindowTiles = document.getElementById('importWindowTiles');
        importWindowTiles.appendChild(draggableTile);
        draggableTile.classList.remove("dragging");
    }
}

var importTiles = document.querySelectorAll(".tile");
importTiles.forEach(function (tile) {
    tile.addEventListener("dragstart", function (event) {
        event.dataTransfer.setData("text/plain", event.target.id);
        event.target.classList.add("dragging");
    });

    tile.addEventListener("dragend", function () {
        this.classList.remove("dragging");
    });
});

function importMoveTile(tile) {
    var importWindowTilesDiv = document.getElementById('importWindowTiles');
    var importTilesDiv = document.getElementById('importTiles');
    if (tile.parentNode === importWindowTilesDiv) {
        importTilesDiv.appendChild(tile);
    } else {
        importWindowTilesDiv.appendChild(tile);
    }
}

function export_import_Tiles(export_import) {
    if (export_import){
        socket.emit('export',getTitleNames(export_import))
    }
    else {
        socket.emit('import',getTitleNames(export_import))
    }
}

function exportDrop(event) {
    event.preventDefault();
    var data = event.dataTransfer.getData("text/plain");
    var draggableTile = document.getElementById(data);
    var targetTile = event.target;
    if (targetTile.classList.contains("tile")) {
        var tempTile = document.createElement("div");
        draggableTile.parentNode.insertBefore(tempTile, draggableTile);
        targetTile.parentNode.insertBefore(draggableTile, targetTile);
        tempTile.parentNode.insertBefore(targetTile, tempTile);
        tempTile.parentNode.removeChild(tempTile);
        draggableTile.classList.remove("dragging");
    } else if (targetTile.classList.contains("tile-container")) {
        var exportWindowTiles = document.getElementById('exportWindowTiles');
        exportWindowTiles.appendChild(draggableTile);
        draggableTile.classList.remove("dragging");
    }
}

var exportTiles = document.querySelectorAll(".tile");
exportTiles.forEach(function (tile) {
    tile.addEventListener("dragstart", function (event) {
        event.dataTransfer.setData("text/plain", event.target.id);
        event.target.classList.add("dragging");
    });

    tile.addEventListener("dragend", function () {
        this.classList.remove("dragging");
    });
});

function exportMoveTile(tile) {
    var exportWindowTilesDiv = document.getElementById('exportWindowTiles');
    var exportTilesDiv = document.getElementById('exportTiles');
    if (tile.parentNode === exportWindowTilesDiv) {
        exportTilesDiv.appendChild(tile);
    } else {
        exportWindowTilesDiv.appendChild(tile);
    }
}

function allowDrop(event) {
    event.preventDefault();
}

function showTable(tableId, buttonId) {
    var toolsTable = document.getElementById(tableId);
    var editButton = document.getElementById(buttonId);

    toolsTable.style.display = toolsTable.style.display === 'table' ? 'none' : 'table';
    editButton.classList.toggle('highlight');
  }