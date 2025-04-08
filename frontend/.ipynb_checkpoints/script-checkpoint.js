const container = document.getElementById("product-container");
fetch("http://localhost:8000/products")
// fetch("http://localhost:8000/products")
  .then(res => res.json())
  .then(data => {
    container.innerHTML = ""; // clear loading text
    data.forEach(product => {
      const el = document.createElement("div");
      el.className = "product";
      el.innerHTML = `
        <h3><a href="${product.url}" target="_blank">${product.name}</a></h3>
        <p>💰 Price: €${parseFloat(product.price).toFixed(2)}</p>
        <p>📅 Last Checked: ${new Date(product.last_checked).toLocaleString()}</p>
        ${
          product.dropped
            ? `<p class="on-sale">🔥 Price dropped from €${product.previous_price.toFixed(2)}!</p>`
            : `<p>Price has not dropped.</p>`
        }
      `;
      container.appendChild(el);
    });
  })
  .catch(err => {
    container.innerHTML = "Failed to load product info.";
    console.error("Error:", err);
  });
