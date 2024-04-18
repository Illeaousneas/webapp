$(document).ready(function() {
    $('#checkButton').click(function() {
        const selectedPolicyId = $('#policyDropdown').val();
        $('#report').empty().html('<div class="text-center"><div class="spinner-border" role="status"></div></div>'); // Add loading indicator

        $.ajax({
            url: '/api/checks/',
            type: 'POST',
            data: {
                'policy_id': selectedPolicyId 
            },
            success: function(response) {
                buildReport(response); 
            },
            error: function(error) {
                console.error("Compliance check error:", error);
                displayError("An error occurred during compliance check."); 
            }
        });
    });
});

function buildReport(complianceData) {
    const reportElement = $('#report');
    reportElement.empty(); // Clear any previous report or loading indicator


    if (Object.keys(complianceData).length === 0) { // Check for an empty report
        displayError("No compliance data found.");
        return;
    }

    for (const sectionTitle in complianceData) {
        let sectionElement = $('<div class="card mb-3">');
        let sectionHeader = $('<div class="card-header">').text(sectionTitle);
        let sectionBody = $('<div class="card-body">');
        let checksList = $('<ul class="list-group list-group-flush">');

        const sectionData = complianceData[sectionTitle]; 
        sectionData.checks.forEach(check => {
            let checkStatus = check.status === 'PASS' ? 'text-success fas fa-check' : 'text-danger fas fa-times-circle';
            let checkItem = $(`<li class="list-group-item ${checkStatus}">`).text(`${check.check_title}: ${check.status}`);

            checksList.append(checkItem); 
        });

        sectionBody.append(checksList);
        sectionElement.append(sectionHeader, sectionBody);
        reportElement.append(sectionElement); 
    }
} 

function displayError(errorMessage) {
    const reportElement = $('#report');
    reportElement.html(`<div class="alert alert-danger">${errorMessage}</div>`);
}
