$(document).ready(function () {

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
        data.data.forEach(function(rowData) {
            var row = document.createElement("tr");
    
            Object.values(rowData).forEach(function(cellData) {
                var cell = document.createElement("td");
                cell.textContent = cellData;
                row.appendChild(cell);
            });
    
            tbody.appendChild(row);
        });
    });


});