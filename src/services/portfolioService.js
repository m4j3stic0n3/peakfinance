// Placeholder for portfolio service
    const portfolioService = {
      async getPortfolio() {
        // Simulate fetching portfolio data
        return new Promise((resolve) => {
          setTimeout(() => {
            resolve({
              portfolio: [
                { symbol: "AAPL", percentage: 20 },
                { symbol: "GOOG", percentage: 15 },
                { symbol: "MSFT", percentage: 15 },
                { symbol: "AMZN", percentage: 10 },
                { symbol: "TSLA", percentage: 10 },
                { symbol: "JPM", percentage: 10 },
                { symbol: "V", percentage: 5 },
                { symbol: "MA", percentage: 5 },
                { symbol: "NVDA", percentage: 5 },
                { symbol: "PYPL", percentage: 5 },
              ],
              historicalPerformance: {
                labels: ["2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"],
                data: [1000, 1200, 1500, 1800, 2200, 2500, 3000, 3500, 4000, 4500],
              },
            });
          }, 500);
        });
      },
    };

    export default portfolioService;
