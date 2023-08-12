# FAQ-Recommendations

Bem-vindo ao repositório FAQ-Recommendations! Esta é uma aplicação no qual utiliza busca semântica para encontrar FAQs semelhantes a uma mensagem

## Motivação

### Cenário
Um atendente inicia o atendimento no chat e conforme a conversa vai desenrolando ele entende qual a demanda e acessa à base de Perguntas Frequentes (FAQ) para pegar a resposta adequada
para passar para o cliente (usuário do chat).

### Desafio
Analisando a conversa entre o atendente e o usuário (cliente), a tecnologia de IA consegue entender qual a demanda, busca automática na base de FAQ qual a resposta e **sugere** automaticamente
para o atendente qual seria a resposta adequada para passar para o cliente.

## Instalação
### Requisitos

<table>
  <tr>
    <td>Python</td>
    <td>Git</td>
  </tr>
  <tr>
    <td>3.11.4 ></td>
    <td>2.41.0</td>
  </tr>
</table>

### Configurando o ambiente

1. Clone este repositório utilizando o comando `git clone https://github.com/Rafael-Fortes/faq-recommendations`
2. Vá para a pasta do projeto e crie um ambiente virtual utilizando o comando `python -m venv venv`
3. Ative o ambiente virtual utilizando o comando `./venv/scripts/activate`
4. instale os requisitos utilizando o comando `pip install -r requirements.txt`

### Baixando os Modelos necessários
1. Entre na pasta src/models/
2. Execute o comando `python -m spacy download pt_core_news_sm` para baixar o modelo NLP para processamento de texto
3. Utilize o comando `git clone https://huggingface.co/neuralmind/bert-large-portuguese-cased` para baixar o modelo de embeddings

# Executando a API
1. Certifique-se de que o ambiente virtual está ativado
2. Utilize o comando `uvicorn main:app` para iniciar a API que estará sendo executada na URL: http://127.0.0.1:8000/

## Como fazer requisições à API
para fazer as requisições basta entrar na seguinte URL:`http://127.0.0.1:8000/get_similarities/{seu texto vai aqui}`, no qual será retornado um JSON com as recomendações do FAQ.