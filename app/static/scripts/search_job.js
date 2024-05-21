//search_job.js

function searchJob() {
    var jobNo = document.getElementById('jobNo').value;

    // Make an AJAX request to fetch data based on job number
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_job_details?jobNo=' + jobNo, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var data = JSON.parse(xhr.responseText);
                // Populate readonly fields with retrieved data
                document.getElementById('title').value = data.title;
                document.getElementById('custName').value = data.custName;
                document.getElementById('vehicleType').value = data.vehicleType;
                // Populate other fields as needed
            } else if (xhr.status === 404) {
                // Handle case where job number does not exist
                alert('Job No tidak dijumpai! Sila pastikan tugas telah wujud.');
                // Clear readonly fields or show an error message
                document.getElementById('title').value = '';
                document.getElementById('custName').value = '';
                document.getElementById('vehicleType').value = '';
                // Clear other fields as needed
            }
        }
    };
    xhr.send();
}