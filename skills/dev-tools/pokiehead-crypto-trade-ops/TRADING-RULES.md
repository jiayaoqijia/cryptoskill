# TRADING-RULES.md — Reglas de Trading Crypto de Sic SI™

_Las reglas que gobiernan cada orden del kit. Nada aquí es teórico: cada regla existe porque pasó algo (la lección está anotada). Última revisión: 2026-10-15._

---

## 1. Capital y riesgo

- **R1 — Dinero de testing hasta que diga el owner.** Depósito base acotado; escalar capital solo con autorización explícita de Chuck. _(estado: depósito 100, +81% acumulado al 11-oct)_
- **R2 — Riel de notional por orden.** Ninguna entrada supera el riel publicado (default $1,000 notional) sin que el owner lo suba por escrito. _Lección 9-oct: la orden de Tuni quedó rail-capped en $998 y así debió ser._
- **R3 — Aislada siempre, cross jamás.** Toda posición en isolated; el margen en riesgo es el margen puesto, no la cuenta.
- **R4 — La liq lejana NO es stop.** "La liq ta lejo" no es un plan de salida; es una estadística de cuánto puedes perder. El stop es el stop.

## 2. Stops (la regla que no se negocia)

- **R5 — Toda posición abre con stop definido ANTES de la entrada.** SL nativo (`presetStopLossPrice` vía `SL_PCT`) o watchdog a mercado. Sin stop no hay entrada.
- **R6 — El stop cubre TODA la posición.** Scope documentado en el journal antes de abrir lotes nuevos. _Lección 9-oct: stop armado para la lota 1 (0.0121) mientras la lota 2 (0.0339) quedaba sin cobertura — error de alcance, no de dirección._
- **R7 — Watchdog idempotente.** Chequeo cada 2 min; flag files + estado en disco; exit-0 silencioso salvo acción. Nunca confiar en la RAM para estado de riesgo.
- **R8 — Prueba de fuego pendiente.** El SL nativo no se usa con dinero serio hasta pasar: short mínimo (~0.001 BTC) con SL +2%, verificación visual en UI de Bitunix, cierre inmediato.

## 3. Entradas y señales

- **R9 — Señal ≠ trade.** Un candidato se publica con entrada/SL/TP calculados; los hipotéticos se separan de los resultados. _Robao de stock-market-signal-automation._
- **R10 — Dry-run primero.** Toda lógica nueva (trigger, ladder, watchdog) corre en paper o con mínimo nocional antes de tamaño real. _(propuesta del bus, vigente)_
- **R11 — Ladder/tiers definidos ANTES de abrir.** Niveles de salida en `ladder_watch.sh` + `.tier-state` en disco; no se inventan salidas a mitad del trade.
- **R12 — Sin señales de terceros sin verificación.** Nada de suscripciones a webhooks/prompts de servicios no auditados. _(lección KamdenAI)_

## 4. Ejecución y verificación

- **R13 — Journal append-only.** Toda orden queda en `bitunix-journal.jsonl`: autor, acción, qty, precio pre, orderId, nota. Sin journal no hay trade.
- **R14 — Fill verificado por API.** Tras cada orden se confirma el fill (delta de margin/disponible) antes de declarar éxito. Nada se da por bueno por el mensaje de la API.
- **R15 — Quién ordena.** El owner ordena directo; terceros (Tuni) pasan por el bot con riel; el agente NUNCA abre posiciones por iniciativa propia ni con dinero sin orden trazable.

## 5. Infraestructura

- **R16 — Trading SOLO por IP residencial.** MEXC y Bitunix bloquean IPs datacenter/VPN (AT&T 45.30.88.207 es la ruta buena).
- **R17 — Bitunix por el host correcto.** `fapi.bitunix.com` (api.bitunix.com = WAF 403). Firma doble SHA-256: GET firma payload vacío, POST firma body JSON compacto.
- **R18 — Un solo bot por cuenta.** Sin watchers duplicados ni instancias paralelas pateando la misma llave.
- **R24 — Endpoints verificados solamente.** Prohibido el probing ciego: ninguna llamada firmada a endpoints no documentados en este kit. Un endpoint nuevo se valida contra la documentación oficial del exchange antes de tocarlo con la llave de producción. _(Lección 13-oct: 4 probes a endpoints inexistentes = llave lockeada 30+ horas, trading ciego)_

## 6. Seguridad

- **R19 — Credenciales 0600 fuera de repos.** Jamás en logs, jamás en el repo, jamás en un mensaje. Mover secretos por archivos base64, nunca Buffer/btoa.
- **R20 — Llave trade-only.** Withdraw OFF verificado en UI antes de escalar capital. _(pendiente confirmación del owner)_
- **R21 — Shell root a terceros solo con aprobación del owner.**

## 7. Comunicación

- **R22 — Alertas explícitas.** SL/TP y cambios de estado anuncian por WhatsApp con announce explícito; silencio = nada pasó.
- **R23 — Cambios de scope se anuncian antes de aplicarse.** Subir un riel, ampliar un stop, escalar capital: primero el anuncio, después el trade.
- **R25 — Validar antes de ingerir.** Nada entra al acta sin fuente primaria confirmada; reportes de segunda mano se marcan NO VERIFICADO hasta que una fuente directa confirme o niegue. _(Lección 14-oct: MS NOW reportó a Patel 'aterrizando en Moscú'; el FBI lo negó y la cadena se corrigió en 4 horas — el poisoning se evita validando en la entrada)_

---

### Changlog de lecciones

| Fecha | Lección | Regla |
|---|---|---|
| 2026-10-05 | Primer ladder, tiers cobran por niveles | R11 |
| 2026-10-07 | KamdenAI: señales de terceros no auditadas | R12 |
| 2026-10-09 | Tuni rail-capped; stop cubría solo lota 1 | R2, R6 |
| 2026-10-10 | Prueba de fuego del SL nativo diseñada | R8 |
| 2026-10-13/14 | Llave lockeada por probing ciego; poisoning MS NOW-Patel en vivo | R24, R25 |

_Repo privado. El código obedece estas reglas; las reglas obedecen a los errores que ya pagamos._
