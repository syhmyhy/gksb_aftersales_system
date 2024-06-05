document.addEventListener('DOMContentLoaded', (event) => {
    const salesUnitInput = document.getElementById('salesUnit');
    const quantityInput = document.getElementById('quantity');
    const totalSalesInput = document.getElementById('totalSales');
    const profitUnitInput = document.getElementById('profitUnit');
    const totalProfitInput = document.getElementById('totalProfit');
    const marginProfitInput = document.getElementById('marginProfit');

    function calculateTotalSales() {
        const salesUnit = parseFloat(salesUnitInput.value) || 0;
        const quantity = parseFloat(quantityInput.value) || 0;
        const totalSales = salesUnit * quantity;
        totalSalesInput.value = totalSales.toFixed(2);
        calculateMarginProfit();
    }

    function calculateTotalProfit() {
        const profitUnit = parseFloat(profitUnitInput.value) || 0;
        const quantity = parseFloat(quantityInput.value) || 0;
        const totalProfit = profitUnit * quantity;
        totalProfitInput.value = totalProfit.toFixed(2);
        calculateMarginProfit();
    }

    function calculateMarginProfit() {
        const totalSales = parseFloat(totalSalesInput.value) || 0;
        const totalProfit = parseFloat(totalProfitInput.value) || 0;
        let marginProfit = 0;

        // Check if the denominator is not zero
        if (totalSales !== totalProfit) {
            marginProfit = (totalProfit / (totalSales - totalProfit)) * 100;
        } else {
            // Handle division by zero scenario
            marginProfit = Infinity; // or any other value or message you prefer
        }

        marginProfitInput.value = marginProfit.toFixed(2);
    }

    function calculateQuantity() {
        const salesUnit = parseFloat(salesUnitInput.value) || 0;
        const totalSales = parseFloat(totalSalesInput.value) || 0;
        let quantity = 0;

        // Check if salesUnit is not zero to avoid division by zero
        if (salesUnit !== 0) {
            quantity = totalSales / salesUnit;
        }

        quantityInput.value = quantity.toFixed(2);
        calculateTotalProfit();
    }

    salesUnitInput.addEventListener('input', calculateTotalSales);
    quantityInput.addEventListener('input', calculateTotalSales);
    profitUnitInput.addEventListener('input', calculateTotalProfit);
    quantityInput.addEventListener('input', calculateTotalProfit);

    salesUnitInput.addEventListener('input', calculateQuantity);
    totalSalesInput.addEventListener('input', calculateQuantity);
});
