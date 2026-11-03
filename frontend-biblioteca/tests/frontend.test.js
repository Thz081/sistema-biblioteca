import { describe, expect, test } from "vitest";
import fs from "node:fs";
import vm from "node:vm";

const script = fs.readFileSync(
  new URL("../script.js", import.meta.url),
  "utf8"
);

function createElement() {
  return {
    textContent: "",
    innerHTML: "",
    value: "",
    type: "password",
    disabled: false,
    dataset: {},

    classList: {
      add() {},
      remove() {},
      toggle() {}
    },

    addEventListener() {},

    onclick: null
  };
}

const elements = {};

const document = {
  querySelector(selector) {
    if (!elements[selector]) {
      elements[selector] = createElement();
    }

    return elements[selector];
  },

  querySelectorAll() {
    return [];
  }
};

const localStorage = {
  getItem() {
    return null;
  },

  setItem() {},

  removeItem() {}
};

const context = {
  window: {
    APP_CONFIG: {
      API_URL: "http://localhost:8000"
    },

    toastTimer: null
  },

  document,
  localStorage,

  fetch: async () => {
    throw new Error("fetch não deve ser chamado neste teste");
  },

  URLSearchParams,

  setTimeout,
  clearTimeout,

  console
};

vm.createContext(context);

vm.runInContext(
  `${script}
   globalThis.testFunctions = {
     initials,
     escapeHtml,
     normalizeBook,
     loadCurrentUser,
     refreshData
   };`,
  context
);

const {
  initials,
  escapeHtml,
  normalizeBook
} = context.testFunctions;

describe("Frontend do Sistema da Biblioteca", () => {

  // ============================================================
  // TESTE PROPOSITALMENTE FALHO
  // ============================================================

  test("deve gerar corretamente as iniciais do título do livro", () => {
    expect(initials("Dom Casmurro")).toBe("DC");
  });


  // ============================================================
  // TESTE NORMAL
  // ============================================================

  test("deve normalizar corretamente os dados de um livro", () => {

    const livro = {
      id: 1,
      titulo: "Dom Casmurro",
      autor: "Machado de Assis",
      categoria_nome: "Romance",
      categoria_id: 2,
      quantidade: 5,
      disponiveis: 3,
      isbn: "123456",
      editora: "Editora X",
      ano_publicacao: 1899
    };

    expect(normalizeBook(livro)).toEqual({
      id: 1,
      title: "Dom Casmurro",
      author: "Machado de Assis",
      category: "Romance",
      categoryId: 2,
      qty: 5,
      available: 3,
      isbn: "123456",
      publisher: "Editora X",
      year: 1899
    });
  });

});

test("leitor carrega sua sessão sem consultar recursos administrativos", async () => {
  const requests = [];
  context.fetch = async (url) => {
    const path = new URL(url).pathname;
    requests.push(path);
    if (["/usuarios", "/dashboard", "/emprestimos"].includes(path)) {
      return { ok: false, json: async () => ({ detail: "Sem permissão" }) };
    }
    return { ok: true, json: async () => path === "/auth/me"
      ? { email: "leitor@example.com", perfil: "LEITOR" } : [] };
  };
  await context.testFunctions.loadCurrentUser();
  await expect(context.testFunctions.refreshData()).resolves.toBeUndefined();
  expect(requests).toContain("/emprestimos/me");
  expect(requests).not.toContain("/usuarios");
  expect(requests).not.toContain("/dashboard");
  expect(requests).not.toContain("/emprestimos");
});
