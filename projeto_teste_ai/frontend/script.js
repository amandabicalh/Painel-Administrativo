function saudar() {
    const nomeInput = document.getElementById('nome');
    const mensagem = document.getElementById('mensagem');
    const nome = nomeInput.value.trim();

    if (nome) {
        mensagem.textContent = `Olá, ${nome}! Bem-vindo ao projeto.`;
    } else {
        mensagem.textContent = 'Por favor, digite seu nome.';
    }
}

async function handleLogin(event) {

    event.preventDefault();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const mensagem = document.getElementById('mensagem');

    if (!email || !password) {
        mensagem.textContent = 'Por favor, preencha todos os campos.';
        mensagem.style.color = 'red';
        return;
    }

    try {

        const resposta = await fetch("http://127.0.0.1:5000/login", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email: email,
                senha: password
            })

        });

        const dados = await resposta.json();

        if (resposta.ok) {

            mensagem.textContent = dados.mensagem;
            mensagem.style.color = "green";

            // salva TOKEN JWT
            localStorage.setItem("token", dados.token);

            // salva email
            localStorage.setItem("usuarioLogado", dados.email);

            setTimeout(() => {
                window.location.href = "dashboard.html";
            }, 1200);

        } else {

            mensagem.textContent = dados.erro || "Erro no login";
            mensagem.style.color = "red";

        }

    } catch (erro) {

        mensagem.textContent = "Erro ao conectar com o servidor.";
        mensagem.style.color = "red";

    }
}

document.getElementById('loginForm').addEventListener('submit', handleLogin);