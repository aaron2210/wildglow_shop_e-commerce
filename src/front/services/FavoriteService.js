import { BACKEND_URL, get_token } from "./Apiconsig";

const FavoriteService = {}

// POST /favoritos (agregar producto a favoritos)
FavoriteService.addFavorito = async (id_producto) => {
  const resp = await fetch(`${BACKEND_URL}/favoritos`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": get_token()
    },
    body: JSON.stringify({ id_producto })
  });
  return await resp.json();
};
// GET /favoritos (obtener mis favoritos)
FavoriteService.getFavoritos = async () => {
  const resp = await fetch(`${BACKEND_URL}/favoritos`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};
// DELETE /favoritos/:id (eliminar favorito por id)
FavoriteService.deleteFavorito = async (id) => {
  const resp = await fetch(`${BACKEND_URL}/favoritos/${id}`, {
    method: "DELETE",
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};

export default FavoriteService;