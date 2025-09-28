import { BACKEND_URL, get_token } from "./Apiconsig";

const UserService = {}

UserService.getUsers = async () => {
    const resp = await fetch(BACKEND_URL + "users", {
        headers: { "Authorization": get_token() }
    })
    return await resp.json()
}

UserService.getUser = async (id) => {
    const resp = await fetch(BACKEND_URL + "users/" + id, {
        headers: { "Authorization": get_token() }
    })
    return await resp.json()
}

UserService.updateUser = async (id, data) => {
    const resp = await fetch(BACKEND_URL + "users/" + id, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": get_token()
        },
        body: JSON.stringify(data)
    })
    return await resp.json()
}

UserService.deleteUser = async (id) => {
    const resp = await fetch(BACKEND_URL + "users/" + id, {
        method: "DELETE",
        headers: { "Authorization": get_token() }
    })
    return await resp.json()
}

export default UserService