# 📝 README

## 👉 Informações gerais

O projeto consiste em um aplicativo Flask que permite o envio de imagens para serem salvas em um diretório. O aplicativo possui uma rota `/envio` que recebe uma imagem, a captura usando a webcam e a salva no diretório `imagens`.

## 🎯 Objetivos

O objetivo deste projeto é demonstrar um exemplo simples de como criar uma rota em Flask para receber e salvar imagens no servidor, aliada com a manipulação de imagens e interação do backend com um sistema de visão computacional.

## 🛠 Estrutura do projeto

A estrutura do projeto é organizada da seguinte forma:

```
.
├── exercício_4
│   ├── app.py
│   ├── imagens
│   │   └── (pasta vazia)
│   └── routes.py
```

A seguir, cada arquivo e pasta do projeto será detalhado:

- **app.py**: Este arquivo contém o código principal para a criação do aplicativo Flask. Ele importa o módulo `Flask` e o blueprint `router` definido no arquivo `routes.py`. O aplicativo é registrado com o blueprint e, em seguida, é executado quando o módulo é chamado diretamente.
- **imagens**: Esta pasta é destinada ao armazenamento das imagens enviadas pelo usuário.
- **routes.py**: Este arquivo define um blueprint chamado `router`, que contém a rota `/envio`. Quando essa rota é acessada via método POST, ocorre a captura de uma imagem da webcam e o salvamento no diretório `imagens`.

## 💻 Uso

Após a instalação e execução do projeto, você poderá enviar uma imagem para ser salva. Para isso, acesse a rota `/envio` no navegador e siga as instruções para capturar e enviar a imagem.
