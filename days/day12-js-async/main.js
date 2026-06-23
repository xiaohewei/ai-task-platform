// Day12 — JS 异步：Promise / fetch / async-await
async function fetchUser(id) {
  const res = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
  return res.json();
}
async function loadAll() {
  const [user1, user2] = await Promise.all([fetchUser(1), fetchUser(2)]);
  console.log(user1.name, user2.name);
}
