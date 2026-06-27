const API_BASE = window.location.origin;

async function fetchItems() {
  const res = await fetch(`${API_BASE}/items/`);
  const data = await res.json();
  return data;
}

function renderItems(items) {
  const container = document.getElementById('items');
  container.innerHTML = '';
  if (!items.length) {
    container.innerHTML = '<p>No items yet.</p>';
    return;
  }
  items.forEach(item => {
    const el = document.createElement('div');
    el.className = 'item';
    el.innerHTML = `
      <div><strong>${item.name}</strong> (ID: ${item.id})</div>
      <div>${item.description || ''}</div>
      <div>Price: ${item.price} Tax: ${item.tax || 0}</div>
      <div class="actions">
        <button data-id="${item.id}" class="edit">Edit</button>
        <button data-id="${item.id}" class="delete">Delete</button>
      </div>
    `;
    container.appendChild(el);
  });
}

async function loadAndRender() {
  try {
    const items = await fetchItems();
    renderItems(items);
  } catch (err) {
    console.error(err);
  }
}

document.getElementById('create-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('name').value.trim();
  const description = document.getElementById('description').value.trim();
  const price = parseFloat(document.getElementById('price').value);
  const taxVal = document.getElementById('tax').value;
  const tax = taxVal ? parseFloat(taxVal) : undefined;

  try {
    const res = await fetch(`${API_BASE}/items/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, description, price, tax })
    });
    if (!res.ok) {
      const err = await res.json();
      alert(`Error: ${err.detail || res.statusText}`);
      return;
    }
    document.getElementById('create-form').reset();
    await loadAndRender();
  } catch (err) {
    alert('Network error');
    console.error(err);
  }
});

document.getElementById('items').addEventListener('click', async (e) => {
  const id = e.target.dataset.id;
  if (!id) return;

  if (e.target.classList.contains('delete')) {
    if (!confirm('Delete this item?')) return;
    await fetch(`${API_BASE}/items/${id}`, { method: 'DELETE' });
    await loadAndRender();
    return;
  }

  if (e.target.classList.contains('edit')) {
    // Simple inline edit using prompt for fast UX
    const name = prompt('New name:');
    if (name === null) return;
    const price = prompt('New price:');
    if (price === null) return;
    const body = { name, price: parseFloat(price) };
    await fetch(`${API_BASE}/items/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    await loadAndRender();
    return;
  }
});

// Initial load
loadAndRender();
