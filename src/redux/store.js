import { configureStore } from '@reduxjs/toolkit';
    import userReducer from './userSlice';
    import portfolioReducer from './portfolioSlice';

    const store = configureStore({
      reducer: {
        user: userReducer,
        portfolio: portfolioReducer,
      },
    });

    export default store;
