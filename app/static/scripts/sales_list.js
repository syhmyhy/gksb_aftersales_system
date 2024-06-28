$(document).ready(function() {
    $('#salesTable').DataTable({
        "paging": true,
        "searching": true,
        "ordering": true,
        "info": true,
        "lengthMenu": [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
        "columnDefs": [
            { "targets": [0, 1], "orderable": false }, // Disable ordering on first and second columns
            { "type": "currency", "targets": [7, 8, 9, 10] } // Apply currency sorting to specific columns
        ],
        "rowCallback": function(row, data, index) {
            $('td:eq(0)', row).html(index + 1); // Re-order the row numbering
        }
    });

    // Re-order row numbers after table initialization
    $('#salesTable').on('order.dt search.dt', function() {
        $('#salesTable').DataTable().column(0, {search:'applied', order:'applied'}).nodes().each(function(cell, i) {
            cell.innerHTML = i + 1;
        });
    }).draw();
});

function exportToExcel() {
    const table = document.getElementById('salesTable');
    const ws = XLSX.utils.table_to_sheet(table);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
    XLSX.writeFile(wb, 'sales_marketing_data.xlsx');
}

function searchTable() {
    var input = document.getElementById("searchInput");
    var filter = input.value.toLowerCase();
    var table = document.getElementById("salesTable");
    var tr = table.getElementsByTagName("tr");

    for (var i = 0; i < tr.length; i++) {
        var td = tr[i].getElementsByTagName("td");
        var match = false;
        for (var j = 0; j < td.length; j++) {
            if (td[j]) {
                if (td[j].innerHTML.toLowerCase().indexOf(filter) > -1) {
                    match = true;
                    break;
                }
            }
        }
        if (match) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }
}