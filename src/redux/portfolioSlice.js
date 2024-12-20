import { createSlice } from '@reduxjs/toolkit';

    const portfolioSlice = createSlice({
      name: 'portfolio',
      initialState: {
        portfolio: [],
        historicalPerformance: {},
      },
      reducers: {
        setPortfolio: (state, action) => {
          state.portfolio = action.payload.portfolio;
          state.historicalPerformance = action.payload.historicalPerformance;
        },
      },
    });

    export const { setPortfolio } = portfolioSlice.actions;
    export default portfolioSlice.reducer;
