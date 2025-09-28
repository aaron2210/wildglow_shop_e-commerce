import { BACKEND_URL, get_token } from "./Apiconsig";

const ReviewService = {}

//Para ADMIN
// GET /reviews (todas las reviews)
ReviewService.getAllReviews = async () => {
  const resp = await fetch(`${BACKEND_URL}/reviews`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};
// GET /reviews/:id (una review por ID)
ReviewService.getReview = async (id) => {
  const resp = await fetch(`${BACKEND_URL}/reviews/${id}`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};
// DELETE /reviews/:id (eliminar review)
ReviewService.deleteReview = async (id) => {
  const resp = await fetch(`${BACKEND_URL}/reviews/${id}`, {
    method: "DELETE",
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};
//PARA CLIENTES
// POST /productos/:id/reviews (crear review de un producto)
ReviewService.createReview = async (productoId, data) => {
  const resp = await fetch(`${BACKEND_URL}/productos/${productoId}/reviews`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": get_token()
    },
    body: JSON.stringify(data)
  });
  return await resp.json();
};
// GET /reviews/mis-reviews (mis reviews)
ReviewService.getMisReviews = async () => {
  const resp = await fetch(`${BACKEND_URL}/reviews/mis-reviews`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};
// PUT /reviews/:id (editar mi review)
ReviewService.updateReview = async (id, data) => {
  const resp = await fetch(`${BACKEND_URL}/reviews/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": get_token()
    },
    body: JSON.stringify(data)
  });
  return await resp.json();
};
// DELETE /reviews/:id (eliminar mi review)
ReviewService.deleteMyReview = async (id) => {
  const resp = await fetch(`${BACKEND_URL}/reviews/${id}`, {
    method: "DELETE",
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};

export default ReviewService;