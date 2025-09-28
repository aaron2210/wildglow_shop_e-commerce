import { BACKEND_URL, get_token } from "./Apiconsig";

const SalesService = {}
// PARA ADMIN

SalesService.getVentas = async () => {
  const resp = await fetch(`${BACKEND_URL}/ventas`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};

SalesService.getVenta = async (id) => {
  const resp = await fetch(`${BACKEND_URL}/ventas/${id}`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};
// PUT /ventas/:id (actualizar estado/envío)
SalesService.updateVenta = async (id, data) => {
  const resp = await fetch(`${BACKEND_URL}/ventas/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": get_token()
    },
    body: JSON.stringify(data)
  });
  return await resp.json();
};
// DELETE /ventas/:id (eliminar venta)
SalesService.deleteVenta = async (id) => {
  const resp = await fetch(`${BACKEND_URL}/ventas/${id}`, {
    method: "DELETE",
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};
// GET /ventas/:id/detalles (detalles de una venta)
SalesService.getDetallesVenta = async (ventaId) => {
  const resp = await fetch(`${BACKEND_URL}/ventas/${ventaId}/detalles`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};
// GET /ventas/:id/detalles/:detalleId (detalle específico)
SalesService.getDetalleVenta = async (ventaId, detalleId) => {
  const resp = await fetch(`${BACKEND_URL}/ventas/${ventaId}/detalles/${detalleId}`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};
// Para CLIENTES
// POST /ventas (crear venta con items)
SalesService.createVenta = async (data) => {
  const resp = await fetch(`${BACKEND_URL}/ventas`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": get_token()
    },
    body: JSON.stringify(data)
  });
  return await resp.json();
};
// GET /ventas/mis-ventas (ventas del cliente actual)
SalesService.getMisVentas = async () => {
  const resp = await fetch(`${BACKEND_URL}/ventas/mis-ventas`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};
// GET /ventas/:id (detalle de una venta del cliente)
SalesService.getMiVenta = async (id) => {
  const resp = await fetch(`${BACKEND_URL}/ventas/${id}`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};
// GET /ventas/:id/detalles (detalles de mi venta)
SalesService.getMisDetallesVenta = async (id) => {
  const resp = await fetch(`${BACKEND_URL}/ventas/${id}/detalles`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};
// GET /ventas/:id/detalles/:detalleId (detalle específico de mi venta)
SalesService.getMiDetalleVenta = async (ventaId, detalleId) => {
  const resp = await fetch(`${BACKEND_URL}/ventas/${ventaId}/detalles/${detalleId}`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};

export default SalesService;