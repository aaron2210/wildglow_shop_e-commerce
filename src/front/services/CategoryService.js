import { BACKEND_URL, get_token } from "./Apiconsig";

const CategoryService = {}

CategoryService.getCategorias = async () => {
  const resp = await fetch(`${BACKEND_URL}/categorias`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};

CategoryService.getCategoria = async (id) => {
  const resp = await fetch(`${BACKEND_URL}/categorias/${id}`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};

CategoryService.createCategoria = async (data) => {
  const resp = await fetch(`${BACKEND_URL}/categorias`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": get_token()
    },
    body: JSON.stringify(data)
  });
  return await resp.json();
};

CategoryService.updateCategoria = async (id, data) => {
  const resp = await fetch(`${BACKEND_URL}/categorias/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": get_token()
    },
    body: JSON.stringify(data)
  });
  return await resp.json();
};

CategoryService.deleteCategoria = async (id) => {
  const resp = await fetch(`${BACKEND_URL}/categorias/${id}`, {
    method: "DELETE",
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};

export default CategoryService