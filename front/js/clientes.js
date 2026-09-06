document.addEventListener(
    "DOMContentLoaded",
    () => {

        if (!estaLogado()) {
            window.location.href =
                "login.html";

            return;
        }

        carregarClientes();
    }
);


async function carregarClientes() {

    const tabela =
        document.getElementById(
            "clientesTableBody"
        );

    try {

        const clientes =
            await apiRequest(
                "/clientes/"
            );

        tabela.innerHTML = "";

        if (clientes.length === 0) {

            tabela.innerHTML = `
                <tr>
                    <td colspan="6">
                        Nenhum cliente cadastrado.
                    </td>
                </tr>
            `;

            return;
        }

        clientes.forEach(
            cliente => {

                tabela.innerHTML += `
                    <tr>
                        <td>${cliente.id}</td>

                        <td>${cliente.nome}</td>

                        <td>
                            ${cliente.telefone || "-"}
                        </td>

                        <td>
                            ${cliente.email || "-"}
                        </td>

                        <td>
                            ${cliente.ativo
                                ? "Ativo"
                                : "Inativo"}
                        </td>

                        <td>
                            <button
                                class="btn btn-danger"
                                onclick="excluirCliente(${cliente.id})"
                            >
                                Excluir
                            </button>
                        </td>
                    </tr>
                `;
            }
        );

    } catch (error) {

        console.error(error);

        tabela.innerHTML = `
            <tr>
                <td colspan="6">
                    ${error.message}
                </td>
            </tr>
        `;
    }
}


async function criarCliente(event) {

    event.preventDefault();

    const dados = {

        nome:
            document.getElementById(
                "nome"
            ).value,

        telefone:
            document.getElementById(
                "telefone"
            ).value || null,

        email:
            document.getElementById(
                "email"
            ).value || null,

        cpf:
            document.getElementById(
                "cpf"
            ).value || null,

        endereco:
            document.getElementById(
                "endereco"
            ).value || null,

        observacoes:
            document.getElementById(
                "observacoes"
            ).value || null
    };

    try {

        await apiRequest(
            "/clientes/",
            {
                method: "POST",
                body: JSON.stringify(dados)
            }
        );

        document.getElementById(
            "clienteForm"
        ).reset();

        carregarClientes();

    } catch (error) {

        alert(error.message);
    }
}


async function excluirCliente(id) {

    const confirmar =
        confirm(
            "Deseja realmente excluir este cliente?"
        );

    if (!confirmar) {
        return;
    }

    try {

        await apiRequest(
            `/clientes/${id}`,
            {
                method: "DELETE"
            }
        );

        carregarClientes();

    } catch (error) {

        alert(error.message);
    }
}