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
        if (totalSales !== totalProfit) {
            marginProfit = (totalProfit / (totalSales - totalProfit)) * 100;
        }
        marginProfitInput.value = marginProfit.toFixed(2);
    }

    salesUnitInput.addEventListener('input', calculateTotalSales);
    quantityInput.addEventListener('input', calculateTotalSales);
    profitUnitInput.addEventListener('input', calculateTotalProfit);
    quantityInput.addEventListener('input', calculateTotalProfit);
});
