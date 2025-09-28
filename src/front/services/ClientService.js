import { BACKEND_URL, get_token } from "./Apiconsig";

const ClientService = {}

ClientService.register = async (data) => {
    const resp = await fetch(BACKEND_URL + "registro", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    return await resp.json()
}

ClientService.login = async (data) => {
    const resp = await fetch(BACKEND_URL + "login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    return await resp.json()
}

ClientService.getProfile = async () => {
    const resp = await fetch(BACKEND_URL + "perfil", {
        headers: { "Authorization": get_token() }
    })
    return await resp.json()
}

ClientService.createProfile = async (data) => {
    const resp = await fetch(BACKEND_URL + "perfil", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": get_token()
        },
        body: JSON.stringify(data)
    })
    return await resp.json()
}

ClientService.updateProfile = async (data) => {
    const resp = await fetch(BACKEND_URL + "perfil", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": get_token()
        },
        body: JSON.stringify(data)
    })
    return await resp.json()
}

export default ClientService