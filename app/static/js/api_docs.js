// Config: what each action needs
const ACTIONS = {
  get_all: { method: 'GET',    url: '/api/todos',    needsId: false, needsBody: false },
  get_one: { method: 'GET',    url: '/api/todos/ID', needsId: true,  needsBody: false },
  create:  { method: 'POST',   url: '/api/todos',    needsId: false, needsBody: true  },
  update:  { method: 'PATCH',  url: '/api/todos/ID', needsId: true,  needsBody: true  },
  delete:  { method: 'DELETE', url: '/api/todos/ID', needsId: true,  needsBody: false },
};

// Method badge colors
const METHOD_COLORS = {
  GET:    'get',
  POST:   'post',
  PATCH:  'patch',
  DELETE: 'delete',
};

// Called when user changes the endpoint dropdown
function onEndpointChange() {
  const action = ACTIONS[document.getElementById('tester-endpoint').value];

  // 1. Update method badge
  const badge = document.getElementById('method-display');
  badge.textContent = action.method;
  badge.className   = `method-display ${METHOD_COLORS[action.method]}`;

  // 2. Show/hide ID row
  document.getElementById('id-row').style.display = action.needsId ? 'flex' : 'none';

  // 3. Show/hide task + completed rows
  document.getElementById('task-row').style.display      = action.needsBody ? 'block' : 'none';
  document.getElementById('completed-row').style.display = action.needsBody ? 'flex'  : 'none';

  // 4. Clear inputs and response
  document.getElementById('tester-id').value     = '';
  document.getElementById('task-input').value    = '';
  document.getElementById('completed-input').checked = false;
  document.getElementById('completed-label').textContent = 'Not completed';
  document.getElementById('id-hint').textContent = '';
  document.getElementById('tester-response-box').style.display = 'none';
}

// Called when user types an ID
async function onIdChange() {
  const action  = document.getElementById('tester-endpoint').value;
  const todoId  = document.getElementById('tester-id').value.trim();
  const hint    = document.getElementById('id-hint');

  // Only auto-fetch when updating
  if (action !== 'update' || !todoId) {
    hint.textContent = '';
    return;
  }

  hint.textContent = 'Fetching...';

  try {
    const res  = await fetch(`/api/todos/${todoId}`, {
      credentials: 'same-origin'
    });

    if (!res.ok) {
      hint.textContent = 'Todo not found.';
      document.getElementById('task-input').value        = '';
      document.getElementById('completed-input').checked = false;
      document.getElementById('completed-label').textContent = 'Not completed';
      return;
    }

    const data = await res.json();
    const todo = data.todo;

    // Pre-fill the fields with the existing todo data
    document.getElementById('task-input').value        = todo.task;
    document.getElementById('completed-input').checked = todo.completed;
    document.getElementById('completed-label').textContent = todo.completed ? 'Completed' : 'Not completed';
    hint.textContent = '✓ Loaded';

  } catch (err) {
    hint.textContent = 'Error fetching todo.';
  }
}

// Called when completed toggle changes 
function onCompletedChange() {
  const checked = document.getElementById('completed-input').checked;
  document.getElementById('completed-label').textContent = checked ? 'Completed' : 'Not completed';
}

// Send the API request
async function sendRequest() {
  const actionKey = document.getElementById('tester-endpoint').value;
  const action    = ACTIONS[actionKey];
  const todoId    = document.getElementById('tester-id').value.trim();
  const task      = document.getElementById('task-input').value.trim();
  const completed = document.getElementById('completed-input').checked;

  // Build the URL
  const url = action.url.replace('ID', todoId || '');

  // Validate ID when needed
  if (action.needsId && !todoId) {
    showResponse(0, { error: 'Please enter a Todo ID.' });
    return;
  }

  // Validate task when needed
  if (action.needsBody && !task) {
    showResponse(0, { error: 'Please enter a task.' });
    return;
  }

  const options = {
    method:      action.method,
    headers:     { 'Content-Type': 'application/json' },
    credentials: 'same-origin'
  };

  // JSON body from the simple inputs
  if (action.needsBody) {
    options.body = JSON.stringify({ task, completed });
  }

  try {
    const res  = await fetch(url, options);
    const data = await res.json();
    showResponse(res.status, data);
  } catch (err) {
    showResponse(0, { error: 'Request failed: ' + err.message });
  }
}

// Show the response
function showResponse(status, data) {
  const box   = document.getElementById('tester-response-box');
  const body  = document.getElementById('tester-response-body');
  const badge = document.getElementById('tester-status-badge');

  box.style.display = 'block';
  body.textContent  = JSON.stringify(data, null, 2);
  badge.textContent = status || 'Error';
  badge.className   = 'status-badge';

  if (status >= 200 && status < 300) badge.classList.add('status-ok');
  else                                badge.classList.add('status-err');
}

// Init on page load
onEndpointChange();