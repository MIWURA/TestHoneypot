var socket = io.connect();

///setInterval(function() {
///    if (socket.connected) {
///       console.log("Connected to server");
///    } else {
///        console.log("Not connected to server");
///    }
///}, 3000);

socket.on("updateResponse_data", function (msg) {
    //console.log("Response_data :: " + msg);
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

            // ตรวจสอบเงื่อนไขและเพิ่มวงกลมตามเงื่อนไข
            if (cellData === "RED!") {
                var circle = document.createElement("span");
                circle.classList.add("circle", "red-circle");
                cell.appendChild(circle);
            } else if (cellData === "YELLOW!") {
                var circle = document.createElement("span");
                circle.classList.add("circle", "yellow-circle");
                cell.appendChild(circle);
            } else if (cellData === "ORANGE!") {
                var circle = document.createElement("span");
                circle.classList.add("circle", "orange-circle");
                cell.appendChild(circle);
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
        margin-right: 5px;
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
