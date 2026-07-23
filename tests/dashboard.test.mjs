import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import vm from 'node:vm';

const html = await readFile(new URL('../index.html', import.meta.url), 'utf8');
const scriptMatch = html.match(/<script>\s*([\s\S]*?)\s*<\/script>/);

assert.ok(scriptMatch, 'dashboard inline script must exist');

const sandbox = {
  Chart: Object.assign(function Chart() {}, { defaults: { font: {} } }),
  URL,
};
vm.createContext(sandbox);
vm.runInContext(scriptMatch[1].replace(/\brender\(\);\s*$/, ''), sandbox);

test('dashboard script parses and preserves finite optional values', () => {
  assert.equal(vm.runInContext('fmtOptional(1250)', sandbox), '1.3K');
  assert.equal(vm.runInContext('pctOptional(2.375)', sandbox), '2.38%');
  assert.equal(vm.runInContext('fmtOptional(NaN)', sandbox), '\u2014');
});

test('video values are escaped and unsafe links are rejected', () => {
  assert.equal(
    vm.runInContext("escHTML('<img src=x onerror=alert(1)>')", sandbox),
    '&lt;img src=x onerror=alert(1)&gt;',
  );
  assert.equal(
    vm.runInContext("safeURL('javascript:alert(1)')", sandbox),
    '',
  );
  assert.equal(
    vm.runInContext("safeURL('https://example.com/video')", sandbox),
    'https://example.com/video',
  );
});
