let tg = window.Telegram.WebApp || null;
let user_id = null, username = null;

if (tg && tg.initDataUnsafe) {
    user_id = tg.initDataUnsafe.user ? tg.initDataUnsafe.user.id : null;
    username = tg.initDataUnsafe.user ? tg.initDataUnsafe.user.username : null;
} else {
    user_id = 7142531263;
    username = "KAHDOW";
}

async function postJSON(url, data) {
    return fetch(url, {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }).then(r => r.json());
}

async function checkAdmin() {
    let res = await postJSON('/api/check_admin', {user_id, username});
    if (res.admin) {
        document.getElementById('admin-panel').style.display = "block";
        initAdmin();
    } else {
        document.getElementById('no-access').style.display = "block";
    }
}

function showTab(tab) {
    document.querySelectorAll('.tab').forEach(e => e.style.display = "none");
    document.getElementById('tab-' + tab).style.display = "block";
    document.querySelectorAll('#tabs button').forEach(e => e.classList.remove('active'));
    document.querySelector('#tabs button[onclick="showTab(\' + tab + '\')"]').classList.add('active');
}

async function initAdmin() {
    showTab("stats");
    let stats = await fetch('/api/stats').then(r => r.json());
    let ul = document.getElementById('stats-list');
    ul.innerHTML = "";
    for (let s of stats.stats) {
        let li = document.createElement('li');
        li.textContent = `${s[0]}: ${s[1]}`;
        ul.appendChild(li);
    }

    let users = await fetch('/api/users').then(r => r.json());
    renderUsers(users.users);

    let groups = await fetch('/api/groups').then(r => r.json());
    renderGroups(groups.groups);

    let help = await fetch('/api/help').then(r => r.json());
    document.getElementById('help-text').value = help.help;

    let plugins = await fetch('/api/plugins').then(r => r.json());
    renderPlugins(plugins.plugins);
}

function renderUsers(users) {
    let tbody = document.querySelector('#users-table tbody');
    tbody.innerHTML = "";
    for (let u of users) {
        let tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${u.id}</td>
          <td>${u.nickname}</td>
          <td><input type="text" value="${u.rank}" onchange="changeRank(${u.id}, this.value)"></td>
          <td>${u.blocked ? "Да" : "Нет"}</td>
          <td>
            <button onclick="blockUser(${u.id})">Блок</button>
            <button onclick="unblockUser(${u.id})">Разблок</button>
          </td>
        `;
        tbody.appendChild(tr);
    }
    window.allUsers = users;
}

function filterUsers() {
    let q = document.getElementById('search-user').value.toLowerCase();
    let users = window.allUsers || [];
    let filtered = users.filter(u => (u.nickname && u.nickname.toLowerCase().includes(q)) || (""+u.id).includes(q));
    renderUsers(filtered);
}

function changeRank(user_id, rank) {
    postJSON('/api/set_user_rank', {user_id, rank});
}

function blockUser(user_id) {
    postJSON('/api/block_user', {user_id}).then(initAdmin);
}
function unblockUser(user_id) {
    postJSON('/api/unblock_user', {user_id}).then(initAdmin);
}

function renderGroups(groups) {
    let tbody = document.querySelector('#groups-table tbody');
    tbody.innerHTML = "";
    for (let g of groups) {
        let tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${g.id}</td>
          <td>${g.title}</td>
          <td>${g.blocked ? "Да" : "Нет"}</td>
          <td>
            <button onclick="blockGroup(${g.id})">Блок</button>
            <button onclick="unblockGroup(${g.id})">Разблок</button>
            <button onclick="leaveGroup(${g.id})">Ливнуть</button>
          </td>
        `;
        tbody.appendChild(tr);
    }
}

function blockGroup(group_id) {
    postJSON('/api/block_group', {group_id}).then(initAdmin);
}
function unblockGroup(group_id) {
    postJSON('/api/unblock_group', {group_id}).then(initAdmin);
}
function leaveGroup(group_id) {
    postJSON('/api/leave_group', {group_id}).then(initAdmin);
}

function saveHelp() {
    let text = document.getElementById('help-text').value;
    postJSON('/api/set_help', {text}).then(initAdmin);
}

function renderPlugins(plugins) {
    let ul = document.getElementById('plugins-list');
    ul.innerHTML = "";
    for (let p of plugins) {
        let li = document.createElement('li');
        li.textContent = p;
        let select = document.createElement('select');
        select.innerHTML = `<option value="1">Вкл</option><option value="0">Выкл</option>`;
        select.onchange = function() {
            postJSON('/api/toggle_plugin', {name: p.split(" ")[0], enabled: select.value}).then(initAdmin);
        };
        li.appendChild(select);
        ul.appendChild(li);
    }
}

function restartBot() {
    postJSON('/api/restart', {});
}

window.onload = checkAdmin;