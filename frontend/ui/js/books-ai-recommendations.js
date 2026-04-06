document.addEventListener("DOMContentLoaded", () => {
  if (!ensureAuthenticated()) {
    return;
  }

  const form = document.getElementById("recommendForm");
  const titleInput = document.getElementById("title");
  const limitInput = document.getElementById("limit");
  const offsetInput = document.getElementById("offset");
  const recommendResults = document.getElementById("recommendResults");
  const recommendMeta = document.getElementById("recommendMeta");
  const recommendPagination = document.getElementById("recommendPagination");

  let latestTitle = "";

  (async () => {
    const user = await fetchCurrentUser();
    if (!user) {
      window.location.href = "/ui/login";
      return;
    }
    applyRoleVisibility(Boolean(user.is_admin));
  })();

  const runRecommendations = async (page = 1) => {
    const title = latestTitle;
    const limitValue = Math.max(1, Number(limitInput.value || 20));
    const offsetValue = (Math.max(1, Number(page || 1)) - 1) * limitValue;
    offsetInput.value = String(offsetValue);

    recommendResults.innerHTML = "";
    recommendMeta.innerHTML = "";

    try {
      const params = new URLSearchParams({
        title,
        limit: String(limitValue),
        offset: String(offsetValue),
      });
      const response = await apiRequest(`/books/recommendations?${params.toString()}`);
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || payload.message || "Recommendations failed");
      }

      const books = payload?.data ?? [];
      const total = Number(payload?.total ?? books.length);
      const message = payload?.message ?? payload?.summary ?? "Recommendations loaded.";
      recommendMeta.appendChild(createNoteCard("AI recommendations", message, `Generated from ${title}`));
      if (!books.length) {
        recommendResults.appendChild(createEmptyState("No recommendation results were returned."));
      } else {
        books.forEach((book) => recommendResults.appendChild(createBookCard(book)));
      }
      renderPagination(recommendPagination, total, limitValue, offsetValue, runRecommendations);
      showToast("Recommendations loaded.", "success");
    } catch (error) {
      showToast(error.message, "error");
      recommendPagination.innerHTML = "";
      recommendResults.appendChild(createEmptyState("Unable to load recommendations."));
    }
  };

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const title = titleInput.value.trim();

    if (!title) {
      showToast("Enter a title first.", "error");
      recommendResults.appendChild(createEmptyState("No title was provided."));
      recommendPagination.innerHTML = "";
      return;
    }

    latestTitle = title;
    runRecommendations(1);
  });
});
