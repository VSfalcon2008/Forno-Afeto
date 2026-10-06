# Forno & Afeto — pedidos de pizza

Protótipo responsivo com páginas de início (`index.html`), cardápio (`cardapio.html`), reserva (`reservas.html`), personalização (`pedido.html`), pagamento demonstrativo (`pagamento.html`) e acompanhamento com chat (`acompanhamento.html`). O servidor usa apenas a biblioteca padrão do Python.

## Abrir no Windows

1. Dê dois cliques em `abrir_site.bat`.
2. O script inicia o servidor Python e abre o site no Chrome (ou no navegador padrão, se o Chrome não estiver instalado nos caminhos usuais).

O script procura o iniciador `py`, o comando `python` e o Python incluído no ambiente local do Codex. Se nenhum estiver disponível, é possível abrir `index.html` diretamente para visualizar e navegar pelo protótipo; para usar o servidor Python, instale Python 3 e abra o `.bat` novamente.

Também é possível iniciar manualmente: abra um terminal nesta pasta `outputs`, execute `python server.py` e acesse `http://127.0.0.1:8000`.

O cardápio lista pizzas salgadas e doces com preços ilustrativos para pizzas grandes de oito fatias. Os botões de sabor abrem a personalização do pedido. A página Nossa casa recebe solicitações de reserva de demonstração. Os pedidos, solicitações e mensagens são mantidos apenas em memória e são apagados quando o servidor é reiniciado.

## Sobre pagamento

Pix, cartão e reservas são demonstrações sem cobrança nem confirmação real. O QR Pix apresentado é ilustrativo e o formulário de cartão não pede senha nem CVV e não envia dados do cartão. A solicitação de reserva não é encaminhada ao restaurante. Para usar reservas ou pagamentos reais, integre um serviço apropriado com validação no servidor. O chat responde com uma mensagem automática demonstrativa; não há atendente real conectado.

As imagens e fontes carregam de serviços externos, portanto precisam de internet no navegador.

## Publicar na web

O arquivo `render.yaml` prepara este protótipo para um serviço Python no Render, com a porta e o endereço de rede configurados para acesso público. Para publicar, salve o conteúdo desta pasta na raiz de um repositório GitHub, crie uma conta no Render e conecte o repositório usando a opção Blueprint. O Render então cria o serviço e fornece um endereço público `onrender.com`.

A configuração seleciona o plano gratuito. Esse modo pode suspender o serviço após períodos sem acessos e levar alguns instantes para responder novamente. Pedidos, mensagens e reservas são demonstrações mantidas temporariamente em memória. O pagamento não é real; antes de usar com clientes, integre armazenamento persistente e um provedor de pagamento real.