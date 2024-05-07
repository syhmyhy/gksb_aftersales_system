// filter_aftersales.js

// Function to filter the aftersales table based on user input
function filterTable() {
    // Declare variables
    var input, filter, table, tr, td, i, j, txtValue;
    input = document.getElementById("filterInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("aftersalesTable");
    tr = table.getElementsByTagName("tr");

    // Initialize count for visible rows
    var visibleRowCount = 0;

    // Loop through all table rows
    for (i = 0; i < tr.length; i++) {
        if (i > 0) { // Skip the table header row (index 0)
            var rowVisible = false;
            // Loop through all table cells in the row
            for (j = 0; j < tr[i].cells.length; j++) {
                td = tr[i].cells[j];
                if (td) {
                    txtValue = td.textContent || td.innerText;
                    txtValue = txtValue.toUpperCase();
                    // Check if the cell content matches the filter
                    if (txtValue.indexOf(filter) > -1) {
                        rowVisible = true;
                        break; // If any cell matches, show the row
                    }
                }
            }
            // Show or hide the row based on visibility flag
            if (rowVisible) {
                tr[i].style.display = ""; // Show the row
                visibleRowCount++; // Increment visible row count
                // Update the row count in the first column for visible rows
                var rowCountCell = tr[i].querySelector(".rowCount");
                if (rowCountCell) {
                    rowCountCell.textContent = visibleRowCount;
                }
            } else {
                tr[i].style.display = "none"; // Hide the row
            }
        }
    }
}

// Function to initialize or reset row count for visible rows
function initializeRowCount() {
    var table = document.getElementById("aftersalesTable");
    var tr = table.getElementsByTagName("tr");
    var visibleRowCount = 0;

    // Loop through all table rows
    for (var i = 0; i < tr.length; i++) {
        if (i > 0 && tr[i].style.display !== "none") {
            // Increment visible row count
            visibleRowCount++;
            // Update the row count in the first column for visible rows
            var rowCountCell = tr[i].querySelector(".rowCount");
            if (rowCountCell) {
                rowCountCell.textContent = visibleRowCount;
            }
        }
    }
}

// Initialize row count on page load
initializeRowCount();
