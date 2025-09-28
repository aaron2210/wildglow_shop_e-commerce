import { BACKEND_URL, get_token } from "./Apiconsig";

const PromotionService = {}
//PARA EL ADMIN

PromotionService.getPromociones = async () => {
  const resp = await fetch(`${BACKEND_URL}/promociones`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};

PromotionService.getPromocion = async (id) => {
  const resp = await fetch(`${BACKEND_URL}/promociones/${id}`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};

PromotionService.createPromocion = async (data) => {
  const resp = await fetch(`${BACKEND_URL}/promociones`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": get_token()
    },
    body: JSON.stringify(data)
  });
  return await resp.json();
};

PromotionService.updatePromocion = async (id, data) => {
  const resp = await fetch(`${BACKEND_URL}/promociones/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": get_token()
    },
    body: JSON.stringify(data)
  });
  return await resp.json();
};

PromotionService.deletePromocion = async (id) => {
  const resp = await fetch(`${BACKEND_URL}/promociones/${id}`, {
    method: "DELETE",
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};

//PARA CLIENTES

PromotionService.aplicarPromocion = async (codigo, items) => {
  const resp = await fetch(`${BACKEND_URL}/promociones/aplicar`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": get_token()
    },
    body: JSON.stringify({ codigo, items })
  });
  return await resp.json();
};

export default PromotionService;