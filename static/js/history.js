document.addEventListener('DOMContentLoaded', function () {
    var data = JSON.parse(document.getElementById('data-json').textContent);

    var tbody = document.getElementById('data-table-body');
    tbody.innerHTML = ''; // Clear existing content

    data.forEach(function (item) {
        var row = document.createElement('tr');

        Object.keys(item).forEach(function (key) {
            var cell = document.createElement('td');
            var cellData = item[key];

            if (key === 'alert') {
                if (cellData === 'RED!') {
                    var circle = document.createElement('span');
                    circle.classList.add('circle', 'red-circle');
                    cell.appendChild(circle);
                } else if (cellData === 'YELLOW!') {
                    var circle = document.createElement('span');
                    circle.classList.add('circle', 'yellow-circle');
                    cell.appendChild(circle);
                } else if (cellData === 'ORANGE!') {
                    var circle = document.createElement('span');
                    circle.classList.add('circle', 'orange-circle');
                    cell.appendChild(circle);
                } else {
                    cell.textContent = cellData;
                }
            } else {
                cell.textContent = cellData;
            }

            row.appendChild(cell);
        });

        tbody.appendChild(row);
    });
});

// CSS
var style = document.createElement('style');
style.innerHTML = `
    .circle {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-left: 5px;
    }

    .red-circle {
        background-color: red;
    }

    .yellow-circle {
        background-color: yellow;
    }

    .orange-circle {
        background-color: orange;
    }
`;
document.head.appendChild(style);
