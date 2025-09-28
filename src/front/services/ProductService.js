import { BACKEND_URL, get_token } from "./Apiconsig";

const ProductService = {}
//Para admin

ProductService.getProductosAdmin = async () => {
  const resp = await fetch(`${BACKEND_URL}/productos`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};

ProductService.getProductoAdmin = async (id) => {
  const resp = await fetch(`${BACKEND_URL}/productos/${id}`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};

ProductService.createProducto = async (data) => {
  const resp = await fetch(`${BACKEND_URL}/productos`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": get_token()
    },
    body: JSON.stringify(data)
  });
  return await resp.json();
};

ProductService.updateProducto = async (id, data) => {
  const resp = await fetch(`${BACKEND_URL}/productos/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": get_token()
    },
    body: JSON.stringify(data)
  });
  return await resp.json();
};

ProductService.deleteProducto = async (id) => {
  const resp = await fetch(`${BACKEND_URL}/productos/${id}`, {
    method: "DELETE",
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};

//Productos + Variantes

ProductService.getVariantesByProducto = async (idProducto) => {
  const resp = await fetch(`${BACKEND_URL}/productos/${idProducto}/variantes`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};

ProductService.getVariante = async (id) => {
  const resp = await fetch(`${BACKEND_URL}/variantes/${id}`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};

ProductService.createVariante = async (idProducto, data) => {
  const resp = await fetch(`${BACKEND_URL}/productos/${idProducto}/variantes`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": get_token()
    },
    body: JSON.stringify(data)
  });
  return await resp.json();
};

ProductService.updateVariante = async (id, data) => {
  const resp = await fetch(`${BACKEND_URL}/variantes/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": get_token()
    },
    body: JSON.stringify(data)
  });
  return await resp.json();
};

ProductService.deleteVariante = async (id) => {
  const resp = await fetch(`${BACKEND_URL}/variantes/${id}`, {
    method: "DELETE",
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};

//Para CLIENTES

ProductService.getProductosPublic = async () => {
  const resp = await fetch(`${BACKEND_URL}/productos`);
  return await resp.json();
};

ProductService.getProductoPublic = async (id) => {
  const resp = await fetch(`${BACKEND_URL}/productos/${id}`);
  return await resp.json();
};

ProductService.buscarProductos = async (query) => {
  const resp = await fetch(`${BACKEND_URL}/productos/buscar?q=${encodeURIComponent(query)}`);
  return await resp.json();
};

ProductService.getVariantesPublic = async (idProducto) => {
  const resp = await fetch(`${BACKEND_URL}/productos/${idProducto}/variantes`);
  return await resp.json();
};

ProductService.getVariantePublic = async (id) => {
  const resp = await fetch(`${BACKEND_URL}/variantes/${id}`);
  return await resp.json();
};

export default ProductService;

