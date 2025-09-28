import { BACKEND_URL, get_token } from "./Apiconsig";

const PaymentService = {}
//PARA ADMIN
// GET /pagos (listar todos los pagos)
PaymentService.getAllPagos = async () => {
  const resp = await fetch(`${BACKEND_URL}/pagos`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};
// GET /pagos/:id (obtener un pago por ID)
PaymentService.getPagoAdmin = async (id) => {
  const resp = await fetch(`${BACKEND_URL}/pagos/${id}`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};
// PUT /pagos/:id (actualizar un pago)
PaymentService.updatePagoAdmin = async (id, data) => {
  const resp = await fetch(`${BACKEND_URL}/pagos/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": get_token()
    },
    body: JSON.stringify(data)
  });
  return await resp.json();
};

// PARA CLIENTES
// POST /pagos (crear pago seguro)
PaymentService.createPago = async (pagoData) => {
  const resp = await fetch(`${BACKEND_URL}/pagos`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": get_token()
    },
    body: JSON.stringify(pagoData)
  });
  return await resp.json();
};
// GET /pagos (listar mis pagos)
PaymentService.getMisPagos = async () => {
  const resp = await fetch(`${BACKEND_URL}/pagos`, {
    headers: { "Authorization": get_token() }
  });
  return await resp.json();
};

export default PaymentService;