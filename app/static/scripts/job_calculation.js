// Wait for the document to fully load before running JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Get references to the input fields
    const quantityInput = document.getElementById('quantity');
    const costUnitInput = document.getElementById('costUnit');
    const profitUnitInput = document.getElementById('profitUnit');
    const totalCostInput = document.getElementById('totalCost');
    const totalProfitInput = document.getElementById('totalProfit');

    // Add event listeners to listen for changes in quantity, costUnit, and profitUnit fields
    quantityInput.addEventListener('input', calculateTotals);
    costUnitInput.addEventListener('input', calculateTotals);
    profitUnitInput.addEventListener('input', calculateTotals);

    // Function to calculate totalCost and totalProfit
    function calculateTotals() {
        // Get values from input fields and convert to numbers
        const quantity = parseInt(quantityInput.value) || 0;
        const costUnit = parseFloat(costUnitInput.value) || 0;
        const profitUnit = parseFloat(profitUnitInput.value) || 0;

        // Calculate total cost and total profit
        const totalCost = quantity * costUnit;
        const totalProfit = quantity * profitUnit;

        // Update the totalCost and totalProfit input fields with calculated values
        totalCostInput.value = totalCost.toFixed(2); // Display totalCost rounded to 2 decimal places
        totalProfitInput.value = totalProfit.toFixed(2); // Display totalProfit rounded to 2 decimal places
    }
});
