(function () {
  const loginForm = document.getElementById("loginForm");
  const registerForm = document.getElementById("registerForm");

  if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const username = document.getElementById("username").value.trim();
      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value;

      try {
        const res = await fetch("/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: username || null,
            email: email || null,
            password,
          }),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || "Login failed");
        }

        setToken(data.access_token);
        await fetchCurrentUser(true);
        toast("Login successful");
        setTimeout(() => {
          window.location.href = "/ui/dashboard";
        }, 300);
      } catch (error) {
        toast(error.message, true);
      }
    });
  }

  if (registerForm) {
    registerForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const username = document.getElementById("regUsername").value.trim();
      const email = document.getElementById("regEmail").value.trim();
      const password = document.getElementById("regPassword").value;

      try {
        const res = await fetch("/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, email, password }),
        });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || "Registration failed");
        }

        toast("Registration successful. Redirecting to login...");
        setTimeout(() => {
          window.location.href = "/ui/login";
        }, 700);
      } catch (error) {
        toast(error.message, true);
      }
    });
  }
})();
