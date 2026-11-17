# Live money checklist (operator)

From `dup-market-radar/docs/LIVE_MONEY.md`:

0. go_ready → ops_ready=true  
1. native build  
2. KuCoin Spot keys in `.env` (never commit)  
3. RADAR_API_KEY + REQUIRE=1  
4. native prefer+fail_closed (not lab-python Docker for capital)  
5. snapshot ok + mtf_ensure_ok  
6. PreSoak / live evidence pack preferred  
7. RADAR_PROFILE=live-money  
8. Auto ON only after dry cycle expectation  
9. Small quote caps  

Futures never in `allowed_sectors` for auto.
