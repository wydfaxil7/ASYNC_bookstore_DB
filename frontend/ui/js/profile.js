(function () {
  const output = document.getElementById("profileOutput");
  const refreshBtn = document.getElementById("refreshProfileBtn");
  const logoutBtn = document.getElementById("logoutBtn");

  async function loadProfile() {
    if (!ensureAuthenticated()) {
      return;
    }

    try {
      const data = await fetchCurrentUser(true);
      if (!data) {
        throw new Error("Failed to load profile");
      }
      applyRoleVisibility(Boolean(data.is_admin));
      output.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
      output.textContent = "Could not load profile.";
      toast(error.message, true);
    }
  }

  refreshBtn.addEventListener("click", loadProfile);

  logoutBtn.addEventListener("click", () => {
    clearSession();
    toast("Logged out");
    setTimeout(() => {
      window.location.href = "/ui/login";
    }, 300);
  });

  loadProfile();
})();
