document.addEventListener("DOMContentLoaded", () => {
  if (!ensureAuthenticated()) {
    return;
  }

  const form = document.getElementById("summaryForm");
  const summaryId = document.getElementById("summaryId");
  const summaryName = document.getElementById("summaryName");
  const summaryResult = document.getElementById("summaryResult");

  (async () => {
    const user = await fetchCurrentUser();
    if (!user) {
      window.location.href = "/ui/login";
      return;
    }
    applyRoleVisibility(Boolean(user.is_admin));
  })();

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    summaryResult.innerHTML = "";

    const params = new URLSearchParams();
    if (summaryId.value.trim()) {
      params.set("id", summaryId.value.trim());
    }
    if (summaryName.value.trim()) {
      params.set("name", summaryName.value.trim());
    }

    if (!params.has("id") && !params.has("name")) {
      showToast("Enter a book ID or name.", "error");
      summaryResult.appendChild(createEmptyState("No book selected for summarization."));
      return;
    }

    try {
      const response = await apiRequest(`/books/summary/search?${params.toString()}`);
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || "Unable to generate the summary.");
      }
      summaryResult.appendChild(createSummaryPanel(payload));
      showToast("Summary generated.", "success");
    } catch (error) {
      showToast(error.message, "error");
      summaryResult.appendChild(createEmptyState("Unable to generate the summary."));
    }
  });
});
