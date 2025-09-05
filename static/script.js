async function postJson(url, data) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error((await res.text()) || 'Request failed');
  return res.json();
}

async function postForm(url, formData) {
  const res = await fetch(url, { method: 'POST', body: formData });
  if (!res.ok) throw new Error((await res.text()) || 'Request failed');
  return res.json();
}

function renderList(el, items) {
  el.innerHTML = '';
  for (const item of items || []) {
    const li = document.createElement('li');
    li.textContent = item;
    el.appendChild(li);
  }
}

function setStatus(message) {
  const el = document.getElementById('status');
  el.textContent = message || '';
}

async function analyze() {
  const btn = document.getElementById('analyze');
  const file = document.getElementById('file');
  const text = document.getElementById('text').value.trim();
  const prompt = document.getElementById('prompt').value.trim();
  const results = document.getElementById('results');

  setStatus('');
  btn.disabled = true;

  try {
    let data;
    if (file.files && file.files[0]) {
      const form = new FormData();
      form.append('file', file.files[0]);
      if (prompt) form.append('prompt', prompt);
      data = await postForm('/api/simplify', form);
    } else {
      if (!text) {
        setStatus('Please paste text or upload a PDF.');
        return;
      }
      data = await postJson('/api/simplify', { text, prompt });
    }

    document.getElementById('summary').textContent = data.summary || '';
    renderList(document.getElementById('key_points'), data.key_points);
    renderList(document.getElementById('obligations'), data.obligations);
    renderList(document.getElementById('risks'), data.risks);
    renderList(document.getElementById('actions'), data.actions);
    renderList(document.getElementById('disclaimers'), data.disclaimers);
    results.classList.remove('hidden');
    setStatus('');
  } catch (err) {
    console.error(err);
    setStatus('Error: ' + (err && err.message ? err.message : 'Something went wrong'));
  } finally {
    btn.disabled = false;
  }
}

document.getElementById('analyze').addEventListener('click', analyze);

