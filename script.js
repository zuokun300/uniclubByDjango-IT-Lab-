const reqItems = document.querySelectorAll('.req-item');
const progressText = document.getElementById('progressText');
const themeToggle = document.getElementById('themeToggle');

function updateProgress() {
  const checked = [...reqItems].filter((item) => item.checked).length;
  progressText.textContent = `Completed ${checked} / ${reqItems.length} items`;
}

reqItems.forEach((item) => item.addEventListener('change', updateProgress));
updateProgress();

themeToggle.addEventListener('click', () => {
  const enabled = document.body.classList.toggle('high-contrast');
  themeToggle.setAttribute('aria-pressed', String(enabled));
});

const form = document.getElementById('aiForm');
const formError = document.getElementById('formError');
const aiOutput = document.getElementById('aiOutput');

form.addEventListener('submit', (event) => {
  event.preventDefault();
  formError.textContent = '';

  const tools = document.getElementById('tools').value.trim();
  const parts = document.getElementById('parts').value.trim();
  const validation = document.getElementById('validation').value.trim();

  if (!tools || !parts || !validation) {
    formError.textContent = 'Please complete all fields before generating the statement.';
    return;
  }

  aiOutput.textContent =
`Declaration on the use of Generative AI:
We declare that we have used GenAI in a limited and acknowledged way.
Tools used: ${tools}
Affected parts: ${parts}
Validation approach: ${validation}`;
});
