const API_URL = "http://127.0.0.1:8000";


function getToken() {
    return localStorage.getItem("token");
}


function salvarToken(token) {
    localStorage.setItem("token", token);
}


function removerToken() {
    localStorage.removeItem("token");
}


function estaLogado() {
    return !!getToken();
}


function headersAutenticacao() {

    const token = getToken();

    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    };
}


async function apiRequest(
    endpoint,
    options = {},
    autenticado = true
) {

    const config = {
        ...options,
        headers: {
            ...(options.headers || {})
        }
    };


    if (autenticado) {

        config.headers = {
            ...config.headers,
            ...headersAutenticacao()
        };

    } else {

        config.headers = {
            "Content-Type": "application/json",
            ...config.headers
        };
    }


    let response;

    try {

        response = await fetch(
            `${API_URL}${endpoint}`,
            config
        );

    } catch (error) {

        console.error(
            "Erro de conexão:",
            error
        );

        throw new Error(
            "Não foi possível conectar com a API."
        );
    }


    const data =
        await response
            .json()
            .catch(() => null);


    if (
        response.status === 401 &&
        autenticado
    ) {

        removerToken();

        window.location.href =
            "login.html";

        throw new Error(
            "Sessão expirada."
        );
    }


    if (!response.ok) {

        throw new Error(
            data?.detail ||
            "Erro ao realizar operação."
        );
    }


    return data;
}


// ==============================
// LOGOUT
// ==============================

function logout() {

    removerToken();

    window.location.href =
        "login.html";
}