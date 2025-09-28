export const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

export const get_token = () => {
    return "Bearer " + localStorage.getItem("token")
}