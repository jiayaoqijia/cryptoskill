# sic-crypto-kit - exchange ops playbook for agents

Playbook real que ejecuta un bot personal (OpenClaw) para operar futuros de BTC con
entradas y salidas escalonadas automatizadas por watchers de cron. Cero prediccion de
mercado: solo niveles, disciplina y automatizacion.

## Resultado documentado (oct 2026)
- Short BTCUSDT ~87k, margen aislado 40x, entrada manual del operador.
- Salida en tiers automatizada: mitad a 85.6k, resto a 85.2k; alerta de SL en 88k.
- Watchers cada 5-15 min con flags idempotentes + archivo de estado; PnL verificado por API.
- Trade completo: cuenta 100 -> 129.56 USDT (+29.56, ~30%).

## Arquitectura
    cron (cada 5m)
      |-- entry_trigger.sh   price >= ENTRY_ABOVE  -> market order + flag
      |-- sl_alert.sh        price >= ALERT_ABOVE  -> alerta de chat (1 vez)
      |-- ladder_watch.sh    state machine 1>2>3   -> cierra tiers, nunca repite
            |-- bitunix_client.py (firma + ordenes + SL nativo)
            |-- precio publico via curl (sin auth)

## Stop-loss: nativo vs alerta (LEER)
- **Nativo (server-side):** pasa SLPRICE al abrir y la exchange sostiene el stop
  aunque tu bot muera: `python3 bitunix_client.py open BTCUSDT SELL OPEN 0.0057 40 88400`
- **Alerta (este kit):** `sl_alert.sh` solo AVISA por chat. Si el host muere, no protege na.
- **Posicion ya abierta:** colocar SL a una posicion existente requiere el endpoint de
  plan-orders (no verificado en este kit). Usalo desde la UI de la exchange.
- **Llave:** trade-only, withdraw OFF - verificalo en la UI, la API no lo reporta.

## Las 5 lecciones caras (ya pagadas)
1. **IP residencial o nada.** MEXC y Bitunix bloquean IPs de datacenter/VPN a nivel red
   (verificado con 2 exits de VPN distintos: las conexiones cuelgan).
2. **Bitunix firma raro.** Doble SHA-256 (ver bitunix_client.py), el host es
   fapi.bitunix.com (api.bitunix.com = WAF 403), y los GET firman con payload vacio.
3. **Idempotencia o muerte.** Cada watcher es exit-0 silencioso salvo cuando actua;
   flag files evitan entradas dobles; el estado de tiers vive en disco y sobrevive reinicios.
4. **SL nativo > alerta.** La alerta depende de tu server; el stop nativo vive en la
   exchange. Ambos: el nativo protege, la alerta despierta humanos.
5. **Riesgo acotado.** Margen aislado, nocional chico, salidas escalonadas. 40x multiplica
   lo bueno y lo malo: no subas el tamano hasta llevar meses de ejecucion limpia.

## Quickstart
    cp config.example ~/.config/bitunix.secret && chmod 600 ~/.config/bitunix.secret
    python3 bitunix_client.py price
    SYMBOL=BTCUSDT ENTRY_ABOVE=87000 ./entry_trigger.sh             # trigger de entrada
    SYMBOL=BTCUSDT ALERT_ABOVE=88000 ./sl_alert.sh                  # alerta de SL
    SYMBOL=BTCUSDT T1_BELOW=85600 T2_BELOW=85200 ./ladder_watch.sh  # salida en tiers

Metelos en cron cada 5 min. Para agentes OpenClaw: usa `openclaw automations` con
delivery announce para recibir las alertas por chat.

## Disclaimer
Educacional. No es consejo financiero. Las claves NUNCA van al repo (lee .gitignore).
Cada quien usa sus propias cuentas y claves de exchange.
