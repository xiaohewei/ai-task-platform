// Day11 — JavaScript 基础：变量、函数、DOM 操作
const tasks = [];
function addTask(title) {
  tasks.push({ id: Date.now(), title, done: false });
  render();
}
function toggleTask(id) {
  const t = tasks.find(t => t.id === id);
  if (t) t.done = !t.done;
  render();
}
function render() {
  const list = document.getElementById('taskList');
  list.innerHTML = tasks.map(t =>
    `<li onclick="toggleTask(${t.id})" style="${t.done ? 'text-decoration:line-through' : ''}">${t.title}</li>`
  ).join('');
}
