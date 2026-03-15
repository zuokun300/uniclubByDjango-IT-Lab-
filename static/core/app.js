function getCsrfToken() {
  const input = document.querySelector('input[name="csrfmiddlewaretoken"]');
  return input ? input.value : "";
}

function applyHighContrastToggle() {
  const toggle = document.querySelector("[data-theme-toggle]");
  if (!toggle) {
    return;
  }

  toggle.addEventListener("click", () => {
    const enabled = document.body.classList.toggle("high-contrast");
    toggle.setAttribute("aria-pressed", String(enabled));
  });
}

function wireRegistrationButtons() {
  function setStatusMessage(status, message, tone) {
    status.textContent = message;
    status.classList.remove("error", "success");
    if (tone) {
      status.classList.add(tone);
    }
  }

  function ensureRegisteredBadge(panel) {
    let badge = panel.querySelector("[data-registration-badge]");
    if (!badge) {
      badge = document.createElement("span");
      badge.className = "status-pill";
      badge.setAttribute("data-registration-badge", "");
      badge.textContent = "Registered";
      const status = panel.querySelector("[data-register-status]");
      panel.insertBefore(badge, status);
    }
  }

  const buttons = document.querySelectorAll("[data-register-button]");
  buttons.forEach((button) => {
    button.addEventListener("click", async () => {
      const card = button.closest("[data-event-card]");
      const panel = button.closest("[data-registration-panel]");
      const status = card.querySelector("[data-register-status]");
      const count = card.querySelector("[data-registration-count]");
      button.disabled = true;
      setStatusMessage(status, "Submitting...");

      try {
        const response = await fetch(button.dataset.url, {
          method: "POST",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCsrfToken(),
          },
        });

        const payload = await response.json();
        if (!response.ok || !payload.ok) {
          throw new Error("Registration failed.");
        }

        setStatusMessage(status, `Registered for ${payload.event}.`, "success");
        if (count) {
          count.textContent = payload.count;
        }
        button.remove();
        ensureRegisteredBadge(panel);
      } catch (error) {
        setStatusMessage(status, "Registration failed.", "error");
        button.disabled = false;
      }
    });
  });
}

function wireCommentForms() {
  const forms = document.querySelectorAll("[data-comment-form]");
  forms.forEach((form) => {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const status = form.querySelector("[data-comment-status]");
      const list = form.parentElement.querySelector("[data-comment-list]");
      const formData = new FormData(form);
      status.textContent = "Posting comment...";

      const response = await fetch(form.action, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCsrfToken(),
        },
        body: formData,
      });
      const payload = await response.json();

      if (!response.ok || !payload.ok) {
        status.textContent = "Comment could not be posted.";
        status.classList.add("error");
        return;
      }

      const empty = list.querySelector(".meta");
      if (empty) {
        empty.remove();
      }

      const item = document.createElement("li");
      const author = document.createElement("strong");
      author.textContent = payload.author;

      const timestamp = document.createElement("span");
      timestamp.className = "meta";
      timestamp.textContent = payload.created_at;

      const content = document.createElement("p");
      content.textContent = payload.content;

      item.append(author, document.createTextNode(" "), timestamp, content);
      list.prepend(item);
      form.reset();
      status.textContent = "Comment posted.";
      status.classList.remove("error");
    });
  });
}

applyHighContrastToggle();
wireRegistrationButtons();
wireCommentForms();
