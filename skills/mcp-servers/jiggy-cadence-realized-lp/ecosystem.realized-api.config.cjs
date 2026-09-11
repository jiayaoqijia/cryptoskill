const { readFileSync } = require('fs');
const key = JSON.parse(readFileSync('/home/ubuntu/.config/cadence-secure/thegraph.json', 'utf8')).api_key;
module.exports = {
  apps: [{
    name: 'realized-api',
    script: './bin/api.js',
    cwd: __dirname,
    env: { GRAPH_API_KEY: key, PORT: '3221' },
  }],
};
