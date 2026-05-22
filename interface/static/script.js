const folderName = document.getElementById("folderName");
const commitList = document.getElementById("commitList");
const logsBody = document.getElementById("logsBody");
const commitSearch = document.getElementById("commitSearch");
const settingsBtn = document.getElementById("settingsBtn");
const toast = document.getElementById("toast");

const repoList = document.getElementById("repoList");
let activeRepo = null;
let currentCommits = [];

function showToast(message) {
	toast.textContent = message;
	toast.classList.add("show");
	setTimeout(() => toast.classList.remove("show"), 1800);
}

function renderLogs(lines) {
	if (!lines.length) {
		logsBody.innerHTML = '<p class="muted">Nenhum log encontrado.</p>';
		return;
	}

	logsBody.innerHTML = `
		<div class="log-lines">${lines.map((line) => `<p>${line}</p>`).join("")}</div>
	`;
}

function renderCommits(commits, query = "") {
	commitList.innerHTML = "";

	const filtered = commits.filter((commit) =>
		commit.message.toLowerCase().includes(query.toLowerCase())
	);

	if (filtered.length === 0) {
		commitList.innerHTML = '<div class="empty-message">Nenhum commit encontrado.</div>';
		return;
	}

	filtered.forEach((commit) => {
		const card = document.createElement("button");
		card.className = "commit-card";
		card.type = "button";
		const title = commit.message && commit.message.trim() ? commit.message : "(sem mensagem)";
		card.innerHTML = `
			<div class="commit-title">${title}</div>
			<div class="commit-meta">${commit.date}</div>
		`;

		card.addEventListener("click", () => {
			showToast("Commit selecionado");
		});

		commitList.appendChild(card);
	});
}

async function fetchJson(url, options = {}) {
	const response = await fetch(url, options);
	const data = await response.json();
	if (!data.success) {
		throw new Error(data.output || "Falha na requisicao");
	}
	return data;
}

async function loadRepositories() {
	const data = await fetchJson("/api/repositories");
	repoList.innerHTML = "";
	activeRepo = null;

	if (!data.repositories.length) {
		repoList.innerHTML = '<li class="repo-empty">Nenhum repositorio.</li>';
		folderName.textContent = "Sem repositorio";
		commitList.innerHTML = '<div class="empty-message">Execute o pull para criar um repositorio.</div>';
		return;
	}

	data.repositories.forEach((repo, index) => {
		const item = document.createElement("li");
		item.className = "repo-item";
		item.dataset.repo = repo.name;
		item.textContent = repo.name;
		if (index === 0) {
			item.classList.add("active");
			activeRepo = repo.name;
			folderName.textContent = repo.name;
		}
		item.addEventListener("click", () => selectRepo(repo.name));
		repoList.appendChild(item);
	});
}

async function loadCommits(repoName) {
	const data = await fetchJson(`/api/repositories/${encodeURIComponent(repoName)}/commits`);
	currentCommits = data.commits;
	renderCommits(currentCommits, commitSearch.value);
}

async function loadLogs() {
	const data = await fetchJson("/api/logs");
	renderLogs(data.logs);
}

async function selectRepo(repoName) {
	document.querySelectorAll(".repo-item").forEach((repo) => {
		repo.classList.toggle("active", repo.dataset.repo === repoName);
	});

	activeRepo = repoName;
	folderName.textContent = repoName;
	commitSearch.value = "";
	await loadCommits(repoName);
}

commitSearch.addEventListener("input", (event) => {
	renderCommits(currentCommits, event.target.value);
});

settingsBtn.addEventListener("click", () => {
	showToast("Configuracoes em breve");
});

(async () => {
	try {
		await loadRepositories();
		if (activeRepo) {
			await loadCommits(activeRepo);
		}
		await loadLogs();
	} catch (error) {
		showToast("Erro ao carregar dados");
	}
})();
