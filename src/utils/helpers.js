// Placeholder for helper functions
    const helpers = {
      formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
      },
    };

    export default helpers;
