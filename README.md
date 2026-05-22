# Gitpy

Gitpy é um projeto de estudo criado para entender melhor como o Git funciona por baixo.

A ideia principal é construir uma espécie de “réplica simplificada” de algumas partes do Git usando Python, junto com uma interface gráfica feita com Django, HTML, CSS e JavaScript.

O projeto não tem como objetivo substituir o Git ou o GitHub Desktop. A proposta é estudar, na prática, como funciona o fluxo de versionamento: criar registros, visualizar histórico, organizar commits e preparar alterações antes de enviar para o repositório remoto.

---

## Ideia do projeto

O Git é uma ferramenta muito poderosa, mas muitas vezes quem está aprendendo usa comandos como `git add`, `git commit` e `git push` sem entender muito bem o que acontece por trás.

O Gitpy nasceu como um laboratório para explorar esse funcionamento.

Em vez de apenas executar comandos prontos, o projeto tenta simular algumas ideias de um sistema de versionamento usando uma estrutura própria chamada `mygit`.

---

## CLI do Gitpy

O projeto possui uma interface de linha de comando própria chamada `gitpy`.

Por ela, é possível executar comandos básicos para interagir com a estrutura interna do projeto.

![Ajuda da CLI do Gitpy](docs/imgs/Captura%20de%20tela%20de%202026-05-22%2014-16-09.png)    
![Processo de worflow do Gitpy](docs/imgs/Captura%20de%20tela%20de%202026-05-22%2014-22-10.png)
![Interface do Gitpy](docs/imgs/Captura%20de%20tela%20de%202026-05-22%2014-24-19.png)


A CLI atualmente possui comandos como:

```txt
init       Cria a estrutura interna mygit e inicia o servidor
status     Mostra o que tem no mygit ativo
commit     Registra um commit dentro do mygit ativo
add        Cria um arquivo .txt dentro do mygit com uma mensagem
log        Mostra o histórico salvo em mygit/log.txt
pull       Exporta o último commit para o repository informado
interface  Abre a interface gráfica do Gitpy
