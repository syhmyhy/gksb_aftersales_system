// sales_calculation.js

document.addEventListener('DOMContentLoaded', function() {
    // Function to calculate totals
    function calculateTotals(quantityInput, unitPriceInput, unitProfitInput, tenderTotalPriceInput, tenderTotalProfitInput, marginProfitInput) {
        const quantity = parseFloat(quantityInput.value) || 0;
        const unitPrice = parseFloat(unitPriceInput.value) || 0;
        const unitProfit = parseFloat(unitProfitInput.value) || 0;

        const tenderTotalPrice = quantity * unitPrice;
        const tenderTotalProfit = quantity * unitProfit;

        tenderTotalPriceInput.value = tenderTotalPrice.toFixed(2);
        tenderTotalProfitInput.value = tenderTotalProfit.toFixed(2);
        calculateMarginProfit(tenderTotalPrice, tenderTotalProfit, marginProfitInput);
    }

    // Function to calculate margin profit
    function calculateMarginProfit(tenderTotalPrice, tenderTotalProfit, marginProfitInput) {
        let marginProfit = 0;

        // Check if the denominator is not zero
        if (tenderTotalPrice !== 0) {
            marginProfit = (tenderTotalProfit / tenderTotalPrice) * 100;
        } else {
            // Handle division by zero scenario
            marginProfit = Infinity; // or any other value or message you prefer
        }

        marginProfitInput.value = isNaN(marginProfit) ? '' : marginProfit.toFixed(2);
    }

    // Attach event listeners and perform initial calculations
    function attachListenersAndCalculate(form) {
        const quantityInput = form.querySelector('#quantity');
        const unitPriceInput = form.querySelector('#unitPrice');
        const unitProfitInput = form.querySelector('#unitProfit');
        const tenderTotalPriceInput = form.querySelector('#tenderTotalPrice');
        const tenderTotalProfitInput = form.querySelector('#tenderTotalProfit');
        const marginProfitInput = form.querySelector('#marginProfit');

        quantityInput.addEventListener('input', function() {
            calculateTotals(quantityInput, unitPriceInput, unitProfitInput, tenderTotalPriceInput, tenderTotalProfitInput, marginProfitInput);
        });

        unitPriceInput.addEventListener('input', function() {
            calculateTotals(quantityInput, unitPriceInput, unitProfitInput, tenderTotalPriceInput, tenderTotalProfitInput, marginProfitInput);
        });

        unitProfitInput.addEventListener('input', function() {
            calculateTotals(quantityInput, unitPriceInput, unitProfitInput, tenderTotalPriceInput, tenderTotalProfitInput, marginProfitInput);
        });

        // Initial calculation on page load
        calculateTotals(quantityInput, unitPriceInput, unitProfitInput, tenderTotalPriceInput, tenderTotalProfitInput, marginProfitInput);
    }

    // Find all forms with the class 'sales-form' and attach listeners
    const salesForms = document.querySelectorAll('.sales-form');
    salesForms.forEach(function(form) {
        attachListenersAndCalculate(form);
    });
});
