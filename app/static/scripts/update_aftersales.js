    // Function to calculate warranty expiration date

    function calculateExpired(inputId, periodId, expiredId) {
        // Get the value of dateDelivered input
        var dateDeliveredValue = document.getElementById(inputId).value;

        // Check if the delivered date is empty or not
        if (dateDeliveredValue !== '') {
            // Split the date manually to ensure it's interpreted as dd/mm/yyyy
            var dateParts = dateDeliveredValue.split('-');
            var year = parseInt(dateParts[0]);
            var month = parseInt(dateParts[1]) - 1; // Subtract 1 to convert to JavaScript's 0-based month index
            var day = parseInt(dateParts[2]);

            // Get the value of warranty period input
            var periodValue = parseInt(document.getElementById(periodId).value);

            // If date is valid and periodValue is a valid number
            if (!isNaN(year) && !isNaN(month) && !isNaN(day) && !isNaN(periodValue)) {
                // Convert dateDelivered to Date object
                var dateDelivered = new Date(year, month, day);
                
                // Calculate the expiration date by adding period to dateDelivered
                dateDelivered.setFullYear(dateDelivered.getFullYear() + periodValue);

                // Format the expiration date as yyyy-mm-dd for HTML date input
                var expired = dateDelivered.toISOString().split('T')[0];

                // Set the value of expired input
                document.getElementById(expiredId).value = expired;
            } else {
                // If date or periodValue is not valid, set expired to empty
                document.getElementById(expiredId).value = '';
            }
            } else {
                // If the delivered date is empty, set expired to empty
                document.getElementById(expiredId).value = '';
            }
        }

function confirmLogout() {
    if (confirm("Adakah anda pasti ingin log keluar?")) {
        window.location.href = "{{ url_for('logout') }}";
    }
}

function confirmUpdate() {
    return confirm("Adakah anda pasti ingin kemaskini rekod kenderaan?");
}
// Add event listeners for other inputs if needed