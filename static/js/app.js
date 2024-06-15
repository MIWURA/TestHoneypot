var socket = io.connect();

///setInterval(function() {
///    if (socket.connected) {
///       console.log("Connected to server");
///    } else {
///        console.log("Not connected to server");
///    }
///}, 3000);

socket.on("updateResponse_data", function (msg) {
    var data = msg;

    // ดึง tbody ของตาราง
    var tbody = document.getElementById("data-table-body");

    // ลบข้อมูลเก่าทั้งหมดใน tbody   
    tbody.innerHTML = "";

    // เพิ่มข้อมูลใหม่ลงใน tbody
    data.data.forEach(function (rowData) {
        var row = document.createElement("tr");

        Object.values(rowData).forEach(function (cellData) {
            var cell = document.createElement("td");

            // ตรวจสอบเงื่อนไขและเพิ่มคลาส CSS ตามเงื่อนไข
            if (cellData === "RED!") {
                var textNode = document.createTextNode(cellData.slice(0, -1));
                var coloredSpan = document.createElement("span");
                coloredSpan.textContent = cellData.slice(-1);
                coloredSpan.classList.add("red-text");
                cell.appendChild(textNode);
                cell.appendChild(coloredSpan);
            } else if (cellData === "YELLOW!") {
                var textNode = document.createTextNode(cellData.slice(0, -1));
                var coloredSpan = document.createElement("span");
                coloredSpan.textContent = cellData.slice(-1);
                coloredSpan.classList.add("yellow-text");
                cell.appendChild(textNode);
                cell.appendChild(coloredSpan);
            } else if (cellData === "ORANGE!") {
                var textNode = document.createTextNode(cellData.slice(0, -1));
                var coloredSpan = document.createElement("span");
                coloredSpan.textContent = cellData.slice(-1);
                coloredSpan.classList.add("orange-text");
                cell.appendChild(textNode);
                cell.appendChild(coloredSpan);
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
    .red-text {
        color: red;
    }

    .yellow-text {
        color: yellow;
    }

    .orange-text {
        color: orange;
    }
`;
document.head.appendChild(style);
