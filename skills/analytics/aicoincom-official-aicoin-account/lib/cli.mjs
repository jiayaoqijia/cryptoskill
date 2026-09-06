#!/usr/bin/env node
// Generic CLI dispatcher — parse `<action> [json-params]` from argv and run a handler.
export function cli(handlers) {
  const [action, ...rest] = process.argv.slice(2);
  if (!action || !handlers[action]) {
    const available = Object.keys(handlers).join(', ');
    console.log(JSON.stringify({
      error: action ? `Unknown action "${action}"` : 'No action specified',
      available_actions: available,
      usage: 'node <script> <action> [json-params]',
    }));
    process.exit(1);
  }
  let params = {};
  if (rest.length) {
    const raw = rest.join(' ');
    try {
      params = JSON.parse(raw);
    } catch {
      console.log(JSON.stringify({
        error: `Invalid JSON parameter: ${raw}`,
        hint: 'Parameters must be a JSON object, e.g.: \'{"symbol":"BTC","interval":"1h"}\'',
        example: `node <script> ${action} '{"key":"value"}'`,
      }));
      process.exit(1);
    }
  }
  handlers[action](params).then(r => console.log(JSON.stringify(r, null, 2))).catch(e => {
    // 运行时错误也输出结构化 JSON(与上面 dispatcher 的报错一致),agent 才能稳定解析、转述给用户;
    // 早先只 console.error(纯文本) 会让 agent 把交易所/网络错误当成非预期输出。
    console.log(JSON.stringify({ error: e?.message || String(e) }));
    process.exit(1);
  });
}
