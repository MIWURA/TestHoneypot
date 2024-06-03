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
        data.data.forEach(function (rowData) {
            var row = document.createElement("tr");

            Object.values(rowData).forEach(function (cellData) {
                var cell = document.createElement("td");

                // ตรวจสอบเงื่อนไขและเพิ่มคลาส CSS ตามเงื่อนไข
                if (cellData === "RED!") {
                    cell.classList.add("red-cell");
                } else if (cellData === "YELLOW!") {
                    cell.classList.add("yellow-cell");
                } else if (cellData === "ORANGE!") {
                    cell.classList.add("orange-cell");
                }

                cell.textContent = cellData;
                row.appendChild(cell);
            });

            tbody.appendChild(row);
        });
    });

    document.addEventListener('DOMContentLoaded', (event) => {
        const sortBySelect = document.getElementById('SORTBY');
        const intableValueSelect = document.getElementById('intable_value');

        sortBySelect.addEventListener('change', function () {
            console.log('SORTBY changed to:', this.value);
            
            const formData = new FormData();
            formData.append('SORTBY', this.value);

            fetch('/update_intable_value', {
                method: 'POST',
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    // Clear the current options
                    intableValueSelect.innerHTML = '';
                    // Add new options
                    data.forEach(item => {
                        const option = document.createElement('option');
                        option.value = item.value;
                        option.textContent = item.text;
                        intableValueSelect.appendChild(option);
                    });
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        });

        intableValueSelect.addEventListener('change', function () {
            const formData = new FormData();
            formData.append('SORTBY', sortBySelect.value);
            formData.append('intable_value', this.value);

            fetch('/Monitor', {
                method: 'POST',
                body: formData
            })
                .then(response => {
                    if (response.redirected) {
                        window.location.href = response.url;
                    }
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        });
    });





});

