(function () {
  if (!ensureAuthenticated()) {
    return;
  }

  const secureButtons = [
    document.getElementById("editBooksSecureBtn"),
    document.getElementById("editBooksSecureCardBtn"),
  ].filter(Boolean);

  (async () => {
    const user = await fetchCurrentUser();
    if (!user) {
      window.location.href = "/ui/login";
      return;
    }

    applyRoleVisibility(Boolean(user.is_admin));

    const hero = document.querySelector(".dashboard-hero");
    if (hero) {
      const roleText = user.is_admin
        ? "You are in admin mode with full book management access."
        : "You are in customer mode. Admin-only actions are hidden.";
      hero.insertAdjacentHTML(
        "beforeend",
        `<div class="note-card"><p class="kicker">READY</p><h3 class="note-title">Choose a page to continue</h3><p class="muted">${roleText}</p></div>`,
      );
    }

    secureButtons.forEach((btn) => {
      btn.addEventListener("click", async (event) => {
        event.preventDefault();
        if (!user.is_admin) {
          showToast("Only admins can access Edit Books.", "error");
          return;
        }

        const password = window.prompt("Confirm your password to open Edit Books:");
        if (!password) {
          return;
        }

        try {
          const response = await fetch("/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              username: user.username || null,
              email: user.email || null,
              password,
            }),
          });
          const payload = await response.json();
          if (!response.ok) {
            throw new Error(payload.detail || "Password verification failed");
          }

          if (payload.access_token) {
            setToken(payload.access_token);
            await fetchCurrentUser(true);
          }
          showToast("Password verified.", "success");
          window.location.href = "/ui/books/edit";
        } catch (error) {
          showToast(error.message || "Password verification failed", "error");
        }
      });
    });
  })();
})();
