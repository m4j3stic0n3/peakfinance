import { createSlice } from '@reduxjs/toolkit';

    const userSlice = createSlice({
      name: 'user',
      initialState: {
        isLoggedIn: false,
        token: null,
        username: null,
      },
      reducers: {
        loginSuccess: (state, action) => {
          state.isLoggedIn = true;
          state.token = action.payload.token;
          state.username = action.payload.username;
        },
        logout: (state) => {
          state.isLoggedIn = false;
          state.token = null;
          state.username = null;
        },
      },
    });

    export const { loginSuccess, logout } = userSlice.actions;
    export default userSlice.reducer;
