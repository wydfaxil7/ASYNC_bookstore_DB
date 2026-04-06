(function () {
  const output = document.getElementById("profileOutput");
  const refreshBtn = document.getElementById("refreshProfileBtn");
  const logoutBtn = document.getElementById("logoutBtn");

  async function loadProfile() {
    if (!ensureAuthenticated()) {
      return;
    }

    try {
      const res = await api("/auth/me");
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Failed to load profile");
      }
      output.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
      output.textContent = "Could not load profile.";
      toast(error.message, true);
    }
  }

  refreshBtn.addEventListener("click", loadProfile);

  logoutBtn.addEventListener("click", () => {
    setToken("");
    toast("Logged out");
    setTimeout(() => {
      window.location.href = "/ui/login";
    }, 300);
  });

  loadProfile();
})();
