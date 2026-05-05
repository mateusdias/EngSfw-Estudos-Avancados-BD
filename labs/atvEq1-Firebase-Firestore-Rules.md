# Atividade em Equipe 1: Firebase Firestore Rules

## Organização

Esta atividade deve ser realizada em **dupla ou trio**.

**Não serão aceitas entregas individuais.**

## Objetivo

Aprender a modelar e implementar regras de segurança do **Cloud Firestore**, controlando acesso de leitura e escrita a documentos de acordo com o usuário autenticado e seu papel no sistema.

Ao final da atividade, a equipe deve ser capaz de:

- compreender a estrutura básica das regras do Firestore;
- diferenciar permissões de leitura, criação, atualização e remoção;
- usar `request.auth`, `resource.data` e `request.resource.data`;
- criar regras baseadas em papéis, como `aluno`, `professor` e `admin`;
- testar cenários permitidos e negados no simulador de regras do Firebase.

## Documentação de Apoio

Antes de implementar, consulte a documentação oficial:

- [Get started with Cloud Firestore Security Rules](https://firebase.google.com/docs/firestore/security/get-started)
- [Structuring Cloud Firestore Security Rules](https://firebase.google.com/docs/firestore/security/rules-structure)
- [Writing conditions for Cloud Firestore Security Rules](https://firebase.google.com/docs/firestore/security/rules-conditions)
- [Get started with Firebase Security Rules](https://firebase.google.com/docs/rules/get-started)
- [Cloud Firestore quickstart](https://firebase.google.com/docs/firestore/quickstart)

## Cenário

A equipe deverá criar regras de segurança para um sistema acadêmico simples usando **Firebase Authentication** e **Cloud Firestore**.

O sistema possui três tipos principais de usuários:

- **Aluno**: pode consultar suas próprias notas e faltas, desde que esteja autenticado.
- **Professor**: pode lançar e atualizar notas e faltas das turmas/disciplinas pelas quais é responsável.
- **Admin**: pode cadastrar usuários, turmas, disciplinas e vínculos entre professores, alunos e turmas.

O foco da atividade está nas regras do Firestore. Não é necessário construir uma aplicação completa, mas a equipe deve criar uma estrutura de documentos coerente e demonstrar, por meio das regras, quais acessos são permitidos ou negados.

## Requisitos Funcionais do Cenário

A equipe deverá considerar, no mínimo, os seguintes comportamentos:

1. Usuários não autenticados não podem acessar dados acadêmicos.
2. Um aluno autenticado pode ler apenas seus próprios dados acadêmicos.
3. Um aluno não pode alterar notas nem faltas.
4. Um professor autenticado pode lançar ou atualizar notas e faltas apenas nas disciplinas/turmas sob sua responsabilidade.
5. Um professor não pode alterar dados de disciplinas/turmas de outro professor.
6. Um admin pode gerenciar cadastros gerais do sistema.
7. Nenhum usuário comum pode se promover para outro papel, por exemplo, mudar seu próprio perfil de `aluno` para `professor` ou `admin`.

## Exemplo de Modelo de Dados

Abaixo está uma sugestão de estrutura. A equipe pode adaptar o modelo, desde que explique suas decisões.

```text
usuarios/{uid}
turmas/{turmaId}
disciplinas/{disciplinaId}
matriculas/{matriculaId}
lancamentos/{lancamentoId}
```

## Exemplos de Documentos

### Usuário Aluno

Documento: `usuarios/aluno_001`

```json
{
  "nome": "Ana Silva",
  "email": "ana.silva@email.com",
  "papel": "aluno",
  "ra": "2026001",
  "ativo": true
}
```

### Usuário Professor

Documento: `usuarios/prof_001`

```json
{
  "nome": "Carlos Pereira",
  "email": "carlos.pereira@email.com",
  "papel": "professor",
  "siape": "998877",
  "ativo": true
}
```

### Usuário Admin

Documento: `usuarios/admin_001`

```json
{
  "nome": "Marina Costa",
  "email": "marina.costa@email.com",
  "papel": "admin",
  "ativo": true
}
```

### Turma

Documento: `turmas/turma_bd_2026_1`

```json
{
  "nome": "Banco de Dados Avançado",
  "semestre": "2026-1",
  "disciplinaId": "bd_avancado",
  "professorId": "prof_001",
  "ativa": true
}
```

### Disciplina

Documento: `disciplinas/bd_avancado`

```json
{
  "nome": "Banco de Dados Avançado",
  "codigo": "BDAVAN",
  "cargaHoraria": 80
}
```

### Matrícula

Documento: `matriculas/mat_001`

```json
{
  "alunoId": "aluno_001",
  "turmaId": "turma_bd_2026_1",
  "status": "ativa",
  "dataMatricula": "2026-02-10"
}
```

### Lançamento de Nota e Falta

Documento: `lancamentos/lanc_001`

```json
{
  "alunoId": "aluno_001",
  "turmaId": "turma_bd_2026_1",
  "disciplinaId": "bd_avancado",
  "professorId": "prof_001",
  "nota": 8.5,
  "faltas": 2,
  "avaliacao": "P1",
  "atualizadoEm": "2026-04-15T19:30:00Z"
}
```

## Ponto de Partida para as Rules

A equipe pode começar a partir do esqueleto abaixo e evoluir as condições.

```js
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    function isSignedIn() {
      return request.auth != null;
    }

    function userDoc() {
      return get(/databases/$(database)/documents/usuarios/$(request.auth.uid));
    }

    function hasRole(role) {
      return isSignedIn() && userDoc().data.papel == role;
    }

    function isAdmin() {
      return hasRole("admin");
    }

    function isProfessor() {
      return hasRole("professor");
    }

    function isAluno() {
      return hasRole("aluno");
    }

    match /usuarios/{userId} {
      allow read: if isAdmin() || (isSignedIn() && request.auth.uid == userId);
      allow create, update, delete: if isAdmin();
    }

    match /disciplinas/{disciplinaId} {
      allow read: if isSignedIn();
      allow create, update, delete: if isAdmin();
    }

    match /turmas/{turmaId} {
      allow read: if isSignedIn();
      allow create, update, delete: if isAdmin();
    }

    match /matriculas/{matriculaId} {
      allow read: if isAdmin()
        || (isAluno() && resource.data.alunoId == request.auth.uid)
        || isProfessor();

      allow create, update, delete: if isAdmin();
    }

    match /lancamentos/{lancamentoId} {
      allow read: if isAdmin()
        || (isAluno() && resource.data.alunoId == request.auth.uid)
        || (isProfessor() && resource.data.professorId == request.auth.uid);

      allow create, update: if isAdmin()
        || (
          isProfessor()
          && request.resource.data.professorId == request.auth.uid
        );

      allow delete: if isAdmin();
    }

    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

## Atenção

O esqueleto acima é apenas um ponto de partida. Ele ainda pode ser melhorado.

A equipe deve avaliar problemas como:

- o professor conseguiria lançar nota em qualquer turma se informasse seu próprio `professorId`?
- como validar se o professor realmente pertence à turma informada?
- como impedir que campos sensíveis sejam alterados indevidamente?
- como validar que `nota` está entre `0` e `10`?
- como validar que `faltas` não é um número negativo?

## Entrega

A equipe deverá entregar:

1. Descrição breve do modelo de dados escolhido.
2. Exemplos de documentos usados nos testes.
3. Arquivo ou trecho completo das regras do Firestore.
4. Lista de pelo menos 6 cenários testados, indicando se cada operação foi permitida ou negada.

## Exemplos de Cenários de Teste

| Cenário | Resultado esperado |
|---|---|
| Usuário não autenticado tenta ler `lancamentos/lanc_001` | Negado |
| Aluno `aluno_001` lê seu próprio lançamento | Permitido |
| Aluno `aluno_002` tenta ler lançamento de `aluno_001` | Negado |
| Aluno tenta alterar sua própria nota | Negado |
| Professor `prof_001` lança nota para aluno de sua turma | Permitido |
| Professor `prof_002` tenta alterar lançamento de `prof_001` | Negado |
| Admin cria uma nova disciplina | Permitido |
| Usuário comum tenta alterar seu próprio campo `papel` para `admin` | Negado |

## Critérios de Avaliação

- Clareza do modelo de dados.
- Correção das regras de acesso.
- Uso adequado de autenticação e papéis.
- Tratamento de casos negados.
- Coerência dos exemplos de documentos.
- Qualidade dos testes apresentados pela equipe.

## Regras de Entrega

Entregar as regras do Firestore **impressas**, com **nome e RA de cada integrante**, no final da aula.
