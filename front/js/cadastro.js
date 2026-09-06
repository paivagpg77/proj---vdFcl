document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form =
            document.getElementById(
                "cadastroForm"
            );

        const message =
            document.getElementById(
                "cadastroMessage"
            );

        if (!form) {
            return;
        }

        form.addEventListener(
            "submit",
            async (event) => {

                event.preventDefault();

                const dados = {

                    nome:
                        document.getElementById(
                            "nome"
                        ).value,

                    email:
                        document.getElementById(
                            "email"
                        ).value,

                    senha:
                        document.getElementById(
                            "senha"
                        ).value,

                    empresa_nome:
                        document.getElementById(
                            "empresa_nome"
                        ).value,

                    empresa_cnpj:
                        document.getElementById(
                            "empresa_cnpj"
                        ).value || null,

                    empresa_telefone:
                        document.getElementById(
                            "empresa_telefone"
                        ).value || null
                };

                message.textContent =
                    "Criando sua conta...";

                message.className =
                    "message";

                try {

                    await apiRequest(
                        "/auth/cadastro",
                        {
                            method: "POST",
                            body: JSON.stringify(dados)
                        },
                        false
                    );

                    message.textContent =
                        "Cadastro realizado com sucesso!";

                    message.className =
                        "message success";

                    form.reset();

                    setTimeout(
                        () => {
                            window.location.href =
                                "login.html";
                        },
                        1000
                    );

                } catch (error) {

                    message.textContent =
                        error.message;

                    message.className =
                        "message error";
                }
            }
        );
    }
);