// Placeholder for auth service
    const authService = {
      async login(username, password) {
        // Simulate login
        return new Promise((resolve) => {
          setTimeout(() => {
            if (username === "user" && password === "password") {
              resolve({ success: true, token: "fake-token" });
            } else {
              resolve({ success: false, message: "Invalid credentials" });
            }
          }, 500);
        });
      },
      async register(username, password) {
        // Simulate registration
        return new Promise((resolve) => {
          setTimeout(() => {
            resolve({ success: true, token: "fake-token" });
          }, 500);
        });
      },
    };

    export default authService;
