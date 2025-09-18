// Detecta si estamos en ngrok o en local
let API;

if (window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost") {
    API = "http://127.0.0.1:8000"; // tu servidor local
} else {
    // Si no es local, usa la URL base del navegador (ngrok)
    API = window.location.protocol + "//" + window.location.host;
}

function abrirEntidad(entidad) {
  const menu = document.getElementById("menu-entidad");
  const form = document.getElementById("formulario");
  const resultado = document.getElementById("resultado");
  form.innerHTML = "";
  resultado.innerHTML = "";

  let botones = "";
  if (entidad === "alimentos") {
    botones = `
      <button onclick="abrirForm('crear','alimentos')">Crear</button>
      <button onclick="abrirForm('listar','alimentos')">Listar</button>
      <button onclick="abrirForm('editar','alimentos')">Editar</button>
      <button onclick="abrirForm('eliminar','alimentos')">Eliminar</button>
      <button onclick="abrirForm('sin-cantidad','alimentos')">Ver con cantidad = 0</button>
      <button onclick="abrirForm('con-cantidad','alimentos')">Ver con cantidad > 0</button>
    `;
  }
  if (entidad === "recetas") {
    botones = `
      <button onclick="abrirForm('crear','recetas')">Crear</button>
      <button onclick="abrirForm('listar','recetas')">Listar</button>
      <button onclick="abrirForm('editar','recetas')">Editar</button>
      <button onclick="abrirForm('eliminar','recetas')">Eliminar</button>
      <button onclick="abrirForm('posibles','recetas')">Recetas que puedo hacer</button>
    `;
  }
  if (entidad === "tiendas") {
    botones = `
      <button onclick="abrirForm('crear','tiendas')">Crear</button>
      <button onclick="abrirForm('listar','tiendas')">Listar</button>
      <button onclick="abrirForm('editar','tiendas')">Editar</button>
      <button onclick="abrirForm('eliminar','tiendas')">Eliminar</button>
    `;
  }
  if (entidad === "alimentos-recetas") {
    botones = `
      <button onclick="abrirForm('crear','alimentos-recetas')">Crear relación</button>
      <button onclick="abrirForm('listar','alimentos-recetas')">Listar relaciones</button>
      <button onclick="abrirForm('editar-cantidad','alimentos-recetas')">Editar cantidad</button>
    `;
  }
  if (entidad === "alimentos-tiendas") {
    botones = `
      <button onclick="abrirForm('crear','alimentos-tiendas')">Crear relación</button>
      <button onclick="abrirForm('listar','alimentos-tiendas')">Listar relaciones</button>
    `;
  }

  menu.innerHTML = `<h2>${entidad}</h2>${botones}`;
}

function abrirForm(tipo, entidad) {
  const form = document.getElementById("formulario");
  form.innerHTML = "";

  // ===== ALIMENTOS =====
  if (tipo === "crear" && entidad === "alimentos") {
    form.innerHTML = `
      <h3>Crear alimento</h3>
      <form id="form-alimento">
        <input name="nombre_alimento" placeholder="Nombre" required><br>
        <input name="cantidad" type="number" placeholder="Cantidad" required><br>
        <input name="caducidad" type="date" placeholder="Caducidad"><br>
        <label><input type="checkbox" name="congelado"> Congelado</label><br>
        <button type="submit">Enviar</button>
      </form>
    `;
    const f = document.getElementById("form-alimento");
    f.addEventListener("submit", async e => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(f).entries());
      if (data.cantidad) data.cantidad = Number(data.cantidad);
      data.congelado = !!f.querySelector("[name=congelado]").checked;

      try {
        const res = await fetch(`${API}/alimentos/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });
        mostrarResultado(await res.json());
      } catch (err) {
        console.error(err);
        mostrarResultado({ error: true, message: err.message });
      }
    });
    return;
  }

  if (tipo === "listar" && entidad === "alimentos") {
    fetch(API + "/alimentos/").then(r => r.json()).then(mostrarResultado);
    return;
  }

  if (tipo === "sin-cantidad" && entidad === "alimentos") {
    fetch(API+"/alimentos/sin_stock/").then(r=>r.json()).then(mostrarResultado);
}
   if (tipo === "con-cantidad" && entidad === "alimentos") {
    fetch(API+"/alimentos/con_stock/").then(r=>r.json()).then(mostrarResultado);
}

  if (tipo === "editar" && entidad === "alimentos") {
    form.innerHTML = `
      <h3>Editar alimento</h3>
      <form id="form-editar-alimento">
        <input name="nombre_alimento" placeholder="Nombre actual" required><br>
        <input name="cantidad" type="number" placeholder="Nueva cantidad"><br>
        <input name="caducidad" type="date" placeholder="Nueva caducidad"><br>
        <button type="submit">Enviar</button>
      </form>
    `;
    const f = document.getElementById("form-editar-alimento");
    f.addEventListener("submit", async e => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(f).entries());
      for (const key in data) {
        if (data[key] === "") delete data[key];
    }
      const endpoint = `${API}/alimentos/nombre/${encodeURIComponent(data.nombre_alimento)}`;
      delete data.nombre_alimento;

      try {
        const res = await fetch(endpoint, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });
        mostrarResultado(await res.json());
      } catch (err) {
        console.error(err);
        mostrarResultado({ error: true, message: err.message });
      }
    });
    return;
  }

  if (tipo === "eliminar" && entidad === "alimentos") {
    form.innerHTML = `
      <h3>Eliminar alimento</h3>
      <form id="form-eliminar-alimento">
        <input name="nombre_alimento" placeholder="Nombre" required><br>
        <button type="submit">Eliminar</button>
      </form>
    `;
    const f = document.getElementById("form-eliminar-alimento");
    f.addEventListener("submit", async e => {
      e.preventDefault();
      const nombre = f.nombre_alimento.value;
      const endpoint = `${API}/alimentos/${encodeURIComponent(nombre)}`;
      try {
        const res = await fetch(endpoint, { method: "DELETE" });
        mostrarResultado(await res.json());
      } catch (err) {
        console.error(err);
        mostrarResultado({ error: true, message: err.message });
      }
    });
    return;
  }

  // ===== RECETAS =====
  if (tipo === "crear" && entidad === "recetas") {
    form.innerHTML = `
      <h3>Crear receta</h3>
      <form id="form-receta">
        <input name="nombre_receta" placeholder="Nombre de la receta" required><br>
        <input name="autor" placeholder="Autor"><br>
        <input name="url" placeholder="URL"><br>
        <button type="submit">Enviar</button>
      </form>
    `;
    const f = document.getElementById("form-receta");
    f.addEventListener("submit", async e => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(f).entries());
      try {
        const res = await fetch(`${API}/recetas/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });
        mostrarResultado(await res.json());
      } catch (err) {
        console.error(err);
        mostrarResultado({ error: true, message: err.message });
      }
    });
    return;
  }

  if (tipo === "listar" && entidad === "recetas") {
    fetch(API + "/recetas/").then(r => r.json()).then(mostrarResultado);
    return;
  }

  if (tipo === "editar" && entidad === "recetas") {
    form.innerHTML = `
      <h3>Editar receta</h3>
      <form id="form-editar-receta">
        <input name="nombre_receta_actual" placeholder="Nombre actual" required><br>
        <input name="nombre_receta" placeholder="Nuevo nombre"><br>
        <input name="autor" placeholder="Nuevo autor"><br>
        <input name="url" placeholder="Nueva URL"><br>
        <button type="submit">Enviar</button>
      </form>
    `;
    const f = document.getElementById("form-editar-receta");
    f.addEventListener("submit", async e => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(f).entries());
      for (const key in data) {
        if (data[key] === "") delete data[key];
    }
      const endpoint = `${API}/recetas/nombre/${encodeURIComponent(data.nombre_receta_actual)}`;
      delete data.nombre_receta_actual;
      try {
        const res = await fetch(endpoint, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });
        mostrarResultado(await res.json());
      } catch (err) {
        console.error(err);
        mostrarResultado({ error: true, message: err.message });
      }
    });
    return;
  }

  if (tipo === "eliminar" && entidad === "recetas") {
  form.innerHTML = `
  <h3>Eliminar receta</h3>
  <form id="form-eliminar-receta">
    <input name="nombre_receta" placeholder="Nombre de la receta" required><br>
    <button type="submit">Eliminar</button>
  </form>
`;

  const f = document.getElementById("form-eliminar-receta");
f.addEventListener("submit", async e => {
  e.preventDefault(); // esto evita el reload
  const nombre = f.nombre_receta.value;
  try {
    const res = await fetch(API + "/recetas/" + encodeURIComponent(nombre), {
      method: "DELETE"
    });
    const data = await res.json();
    mostrarResultado(data);
  } catch (err) {
    console.error(err);
    mostrarResultado({ error: true, message: err.message });
  }
});
}

    if (tipo === "posibles" && entidad === "recetas") {
    fetch(API + "/recetas/con_alimentos_disponibles/").then(r => r.json()).then(mostrarResultado);
}


  // ===== TIENDAS =====
  if (tipo === "crear" && entidad === "tiendas") {
    form.innerHTML = `
      <h3>Crear tienda</h3>
      <form id="form-tienda">
        <input name="nombre_tienda" placeholder="Nombre de la tienda" required><br>
        <input name="pagina_web" placeholder="Página web"><br>
        <input name="lugar" placeholder="Lugar"><br>
        <button type="submit">Enviar</button>
      </form>
    `;
    const f = document.getElementById("form-tienda");
    f.addEventListener("submit", async e => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(f).entries());
      try {
        const res = await fetch(`${API}/tiendas/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });
        mostrarResultado(await res.json());
      } catch (err) {
        console.error(err);
        mostrarResultado({ error: true, message: err.message });
      }
    });
    return;
  }

  if (tipo === "listar" && entidad === "tiendas") {
    fetch(API + "/tiendas/").then(r => r.json()).then(mostrarResultado);
    return;
  }

  if (tipo === "editar" && entidad === "tiendas") {
    form.innerHTML = `
      <h3>Editar tienda</h3>
      <form id="form-editar-tienda">
        <input name="nombre_tienda_actual" placeholder="Nombre actual" required><br>
        <input name="nombre_tienda" placeholder="Nuevo nombre"><br>
        <input name="pagina_web" placeholder="Nueva página web"><br>
        <input name="lugar" placeholder="Nuevo lugar"><br>
        <button type="submit">Enviar</button>
      </form>
    `;
    const f = document.getElementById("form-editar-tienda");
    f.addEventListener("submit", async e => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(f).entries());
    for (const key in data) {
        if (data[key] === "") delete data[key];
    }
      const endpoint = `${API}/tiendas/nombre/${encodeURIComponent(data.nombre_tienda_actual)}`;
      delete data.nombre_tienda_actual;
      try {
        const res = await fetch(endpoint, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });
        mostrarResultado(await res.json());
      } catch (err) {
        console.error(err);
        mostrarResultado({ error: true, message: err.message });
      }
    });
    return;
  }

  if (tipo === "eliminar" && entidad === "tiendas") {
    form.innerHTML = `
      <h3>Eliminar tienda</h3>
      <form id="form-eliminar-tienda">
        <input name="nombre_tienda" placeholder="Nombre de la tienda" required><br>
        <button type="submit">Eliminar</button>
      </form>
    `;
    const f = document.getElementById("form-eliminar-tienda");
    f.addEventListener("submit", async e => {
      e.preventDefault();
      const nombre = f.nombre_tienda.value;
      const endpoint = `${API}/tiendas/${encodeURIComponent(nombre)}`;
      try {
        const res = await fetch(endpoint, { method: "DELETE" });
        mostrarResultado(await res.json());
      } catch (err) {
        console.error(err);
        mostrarResultado({ error: true, message: err.message });
      }
    });
    return;
  }

  // ===== ALIMENTO-RECETA =====
  if (tipo === "crear" && entidad === "alimentos-recetas") {
    form.innerHTML = `
      <h3>Crear relación alimento-receta</h3>
      <form id="form-alimento-receta">
        <input name="alimento" placeholder="Nombre del alimento" required><br>
        <input name="receta" placeholder="Nombre de la receta" required><br>
        <input name="cantidad" type="number" placeholder="Cantidad" value="1" required><br>
        <button type="submit">Enviar</button>
      </form>
    `;
    const f = document.getElementById("form-alimento-receta");
    f.addEventListener("submit", async e => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(f).entries());
      if (data.cantidad) data.cantidad = Number(data.cantidad);
      const endpoint = `${API}/alimentos/${encodeURIComponent(data.alimento)}/recetas/${encodeURIComponent(data.receta)}?cantidad=${data.cantidad}`;
      try {
        const res = await fetch(endpoint, { method: "POST" });
        const text = await res.text();
        let payload;
        try { payload = JSON.parse(text); } catch { payload = text; }
        mostrarResultado(payload);
      } catch (err) {
        console.error(err);
        mostrarResultado({ error: true, message: err.message });
      }
    });
    return;
  }

  // ===== ALIMENTO-TIENDA =====
  if (tipo === "crear" && entidad === "alimentos-tiendas") {
  form.innerHTML = `
    <h3>Crear relación alimento-tienda</h3>
    <form id="form-relacion">
      <input name="alimento" placeholder="Alimento" required><br>
      <input name="tienda" placeholder="Tienda" required><br>
      <button type="submit">Enviar</button>
    </form>
  `;

  const f = document.getElementById("form-relacion");
  f.addEventListener("submit", async e => {
    e.preventDefault();
    const fd = new FormData(f);

    const alimento = fd.get("alimento").trim();
    const tienda = fd.get("tienda").trim();

    if (!alimento || !tienda) {
      mostrarResultado({ error: true, message: "Debe rellenar ambos campos" });
      return;
    }

    const endpoint = `${API}/alimentos/${encodeURIComponent(alimento)}/tiendas/${encodeURIComponent(tienda)}`;

    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
      });
      const text = await res.text();
      let payload;
      try { payload = JSON.parse(text); } catch { payload = text; }

      if (!res.ok) {
        mostrarResultado({ error: true, status: res.status, body: payload });
      } else {
        mostrarResultado(payload);
      }
    } catch (err) {
      console.error(err);
      mostrarResultado({ error: true, message: err.message });
    }
  });
}

// Listar relaciones alimento-receta
if (tipo === "listar" && entidad === "alimentos-recetas") {
    fetch(API + "/alimentos-recetas/")
        .then(r => r.json())
        .then(mostrarResultado);
}

// Listar relaciones alimento-tienda
if (tipo === "listar" && entidad === "alimentos-tiendas") {
    fetch(API + "/alimentos-tiendas/")
        .then(r => r.json())
        .then(mostrarResultado);
}


}

function mostrarResultado(data) {
  document.getElementById("resultado").textContent = JSON.stringify(data, null, 2);
}