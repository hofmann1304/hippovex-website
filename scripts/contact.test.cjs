const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '..', 'contact.js'), 'utf8');

function fixture(fetchImpl, options = {}) {
  const calls = [];
  const timers = [];
  const attrs = new Map();
  const button = { textContent: 'Anfrage senden', disabled: false };
  const status = { hidden: true, dataset: {}, textContent: '', focused: false,
    setAttribute(key, value) { this[key] = value; }, focus() { this.focused = true; } };
  const form = {
    action: 'https://form.taxi/s/3retq47d', value: 'tester@example.test', resetCount: 0,
    querySelector(selector) { return selector === '[type="submit"]' ? button : status; },
    reportValidity() { return options.valid !== false; },
    addEventListener(name, handler) { this[name] = handler; },
    setAttribute(key, value) { attrs.set(key, value); },
    removeAttribute(key) { attrs.delete(key); },
    reset() { this.resetCount++; this.value = ''; },
  };
  const context = {
    document: { documentElement: { lang: options.lang || 'de' }, querySelector() { return form; } },
    FormData: class { constructor(value) { this.form = value; } },
    AbortController,
    setTimeout(callback) { timers.push(callback); return timers.length; },
    clearTimeout() {},
    fetch(...args) { calls.push(args); return fetchImpl(...args); },
  };
  vm.runInNewContext(source, context);
  return { form, button, status, attrs, calls, timers,
    submit: () => form.submit({ preventDefault() {} }) };
}

test('confirmed submission uses the backend JSON contract and resets the form', async () => {
  const f = fixture(async () => ({ ok: true, json: async () => ({ success: true }) }));
  await f.submit();
  assert.equal(f.calls.length, 1);
  const [url, request] = f.calls[0];
  assert.equal(url, 'https://form.taxi/s/3retq47d');
  assert.equal(request.method, 'POST');
  assert.equal(request.headers.Accept, 'application/json');
  assert.equal(request.credentials, 'omit');
  assert.equal(request.body.form, f.form);
  assert.equal(f.form.resetCount, 1);
  assert.equal(f.status.dataset.state, 'success');
  assert.match(f.status.textContent, /übermittelt/);
  assert.equal(f.status.focused, true);
  assert.equal(f.button.disabled, false);
  assert.equal(f.attrs.has('aria-busy'), false);
});

for (const [name, response] of [
  ['backend rejection', { ok: true, json: async () => ({ success: false }) }],
  ['non-JSON response', { ok: true, json: async () => { throw new Error('HTML instead of JSON'); } }],
  ['HTTP failure despite a success flag', { ok: false, json: async () => ({ success: true }) }],
]) {
  test(name + ' preserves the request and never claims success', async () => {
    const f = fixture(async () => response);
    await f.submit();
    assert.equal(f.status.dataset.state, 'error');
    assert.match(f.status.textContent, /nicht bestätigt/);
    assert.equal(f.form.value, 'tester@example.test');
    assert.equal(f.form.resetCount, 0);
    assert.equal(f.button.disabled, false);
  });
}

test('network failures preserve user input and allow a deliberate later retry', async () => {
  const f = fixture(async () => { throw new Error('Network down'); });
  await f.submit();
  assert.equal(f.calls.length, 1);
  assert.equal(f.form.resetCount, 0);
  assert.equal(f.status.role, 'alert');
  assert.equal(f.button.textContent, 'Anfrage senden');
  assert.equal(f.button.disabled, false);
});

test('invalid forms are never transmitted', async () => {
  const f = fixture(async () => { throw new Error('Must not run'); }, { valid: false });
  await f.submit();
  assert.equal(f.calls.length, 0);
});

test('double submission while pending makes only one request', async () => {
  let finish;
  const pending = new Promise(resolve => { finish = resolve; });
  const f = fixture(() => pending);
  const first = f.submit();
  await f.submit();
  assert.equal(f.calls.length, 1);
  assert.equal(f.button.disabled, true);
  finish({ ok: true, json: async () => ({ success: true }) });
  await first;
  assert.equal(f.form.resetCount, 1);
});

test('timeout aborts the pending request without retrying or deleting entries', async () => {
  const f = fixture((url, request) => new Promise((resolve, reject) => {
    request.signal.addEventListener('abort', () => reject(new Error('Aborted')));
  }));
  const pending = f.submit();
  f.timers[0]();
  await pending;
  assert.equal(f.calls.length, 1);
  assert.equal(f.status.dataset.state, 'error');
  assert.equal(f.form.resetCount, 0);
  assert.equal(f.button.disabled, false);
});

test('English page uses English status text', async () => {
  const f = fixture(async () => ({ ok: true, json: async () => ({ success: true }) }), { lang: 'en' });
  await f.submit();
  assert.match(f.status.textContent, /Your request has been submitted/);
});
