(function () {
  if (!ensureAuthenticated()) {
    return;
  }

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
  })();
})();
