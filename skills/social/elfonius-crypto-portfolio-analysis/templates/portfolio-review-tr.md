# Kripto & Web3 Portföy İncelemesi

**Tarih:** {{AS_OF}}  
**Ana para birimi:** {{BASE_CURRENCY}}  
**Veri kapsamı:** {{DATA_COVERAGE}}  
**Benchmark:** {{BENCHMARK}}  
**Mod:** Tam inceleme

## 1. Yönetici Özeti

- **Ana bulgu:** {{MAIN_FINDING}}
- **Neden önemli:** {{WHY_IT_MATTERS}}
- **Doğrulanan:** {{VERIFIED_POINTS}}
- **Doğrulanamayan:** {{UNVERIFIED_POINTS}}
- **Karar:** {{DECISION}}
- **Görüşü değiştirecek şey:** {{FALSIFIERS}}

## 2. Yetki, IPS-lite ve Kapsam

| Alan | Bilgi |
|---|---|
| Amaç | {{PURPOSE}} |
| Getiri hedefi | {{RETURN_OBJECTIVE}} |
| Risk toleransı | {{RISK_TOLERANCE}} |
| Ufuk | {{HORIZON}} |
| Likidite | {{LIQUIDITY_NEED}} |
| Vergi/hukuk | {{TAX_LEGAL}} |
| Karar verici | {{DECISION_MAKER}} |
| İnceleme döngüsü | {{REVIEW_CYCLE}} |

## 3. Portföy Anlık Görüntüsü

| Pozisyon | Miktar | Fiyat | Değer | Ağırlık | Kaynak/tarih | Kanıt |
|---|---:|---:|---:|---:|---|---|
| {{POSITION}} | {{QTY}} | {{PRICE}} | {{VALUE}} | {{WEIGHT}} | {{SOURCE}} | {{EVIDENCE}} |

**Toplam:** {{TOTAL_VALUE}}  
**Top-1 / Top-2 / Top-3:** {{TOP1}} / {{TOP2}} / {{TOP3}}  
**HHI:** {{HHI}}  
**Küme haritası:** {{CLUSTER_MAP}}

## 4. Performans ve Atıf

| Ölçü | Değer | Dönem | Benchmark | Kanıt |
|---|---:|---|---|---|
| TWR | {{TWR}} | {{TWR_WINDOW}} | {{BENCHMARK}} | {{TWR_EVIDENCE}} |
| MWR | {{MWR}} | {{MWR_WINDOW}} | — | {{MWR_EVIDENCE}} |
| Getiri katkısı | {{CONTRIBUTION}} | {{CONTRIBUTION_WINDOW}} | — | {{CONTRIBUTION_EVIDENCE}} |

> Bir yıldan kısa dönem yıllıklandırılmaz. Maliyet yoksa `P&L değerlendirilemez` yazılır.

## 5. Risk Panosu

| Ölçü | Değer | Dönem | Yöntem | Sınır |
|---|---:|---|---|---|
| Volatilite | {{VOLATILITY}} | {{VOL_WINDOW}} | Tarihsel | {{VOL_LIMIT}} |
| Maks. drawdown | {{MAX_DRAWDOWN}} | {{DD_WINDOW}} | Günlük | {{DD_LIMIT}} |
| VaR 95% 1g | {{VAR}} | {{VAR_WINDOW}} | Tarihsel | {{VAR_LIMIT}} |
| CVaR 95% 1g | {{CVAR}} | {{CVAR_WINDOW}} | Tarihsel | {{CVAR_LIMIT}} |
| Beta | {{BETA}} | {{BETA_WINDOW}} | OLS | {{BETA_LIMIT}} |
| En büyük risk katkısı | {{RISK_CONTRIB}} | {{RC_WINDOW}} | Bileşen CVaR | {{RC_LIMIT}} |

**VaR sınırı:** VaR “maksimum kayıp” değildir; kuyruk, likidite ve rejim riskini tek başına kapsamaz.

## 6. Likidite ve Çıkış

| Pozisyon | Değer | Günlük işlem hacmi | %1 gün | %5 gün | %10 gün | Kilit/kuyruk |
|---|---:|---:|---:|---:|---:|---|
| {{POSITION}} | {{VALUE}} | {{VOLUME}} | {{D1}} | {{D5}} | {{D10}} | {{LOCK}} |

**Stres likiditesi:** {{STRESS_LIQUIDITY}}  
**İlk çıkamayan pozisyon:** {{FIRST_ILLIQUID}}

## 7. Varlık Bazlı Bulgular

### {{ASSET_NAME}}

- **Tez:** {{THESIS}}
- **Tokenomics:** arz/dolaşım/FDV/emisyon/kilit: {{TOKENOMICS}}
- **Değer yakalama:** {{VALUE_CAPTURE}}
- **Gelir/fee:** {{REVENUE}}
- **Konsantrasyon:** {{CONCENTRATION}}
- **Risk:** {{RISK}}
- **Kanıt:** {{EVIDENCE}}

## 8. DeFi ve On-chain

| Pozisyon | Tür | Teminat/borç veya LP | Sağlık/LTV | Oracle | Olay geçmişi | Çıkış |
|---|---|---|---:|---|---|---|
| {{DEFI_POSITION}} | {{TYPE}} | {{COLLATERAL_DEBT}} | {{HEALTH}} | {{ORACLE}} | {{INCIDENTS}} | {{EXIT}} |

**Kontagyon yolu:** {{CONTAGION_PATH}}  
**On-chain akış:** {{ONCHAIN_FLOW}}

## 9. Piyasa Rejimi ve Senaryolar

| Senaryo | Şoklar | Portföy kaybı | En kötü pozisyon | İlk ihlal |
|---|---|---:|---|---|
| Risk-off | BTC −30%, ETH −40% | {{LOSS_1}} | {{WORST_1}} | {{BREACH_1}} |
| Stablecoin depeg | %5 / %20 | {{LOSS_2}} | {{WORST_2}} | {{BREACH_2}} |
| Likidite şoku | Hacim %25 | {{LOSS_3}} | {{WORST_3}} | {{BREACH_3}} |
| Reverse stress | {{REVERSE_SHOCKS}} | {{LOSS_4}} | {{WORST_4}} | {{BREACH_4}} |

## 10. Alternatifler ve Rebalans

| Alternatif | Risk | Likidite | Konsantrasyon | Maliyet/vergi | Ne zaman yanlış olur? |
|---|---|---|---|---|---|
| Mevcut | {{RISK_CURRENT}} | {{LIQ_CURRENT}} | {{CONC_CURRENT}} | {{COST_CURRENT}} | {{FALSIFY_CURRENT}} |
| Risk-azaltılmış | {{RISK_LOW}} | {{LIQ_LOW}} | {{CONC_LOW}} | {{COST_LOW}} | {{FALSIFY_LOW}} |
| Tez içinde çeşitlendirilmiş | {{RISK_DIV}} | {{LIQ_DIV}} | {{CONC_DIV}} | {{COST_DIV}} | {{FALSIFY_DIV}} |

**Rebalans bandı:** {{REBALANCE_BANDS}}  
**Vergi/maliyet notu:** {{TAX_COST_NOTE}}

## 11. Karar Kaydı

- **Karar:** {{DECISION}}
- **Gerekçe:** {{RATIONALE}}
- **Boyut/uygulama:** yalnızca kısıtlar varsa {{SIZE_RANGE}}
- **Falsifier:** {{FALSIFIERS}}
- **İzleme tarihi:** {{REVIEW_DATE}}

## 12. Kaynaklar ve Sınırlamalar

- {{SOURCE_TABLE}}
- **Doğrulanamayan:** {{LIMITATIONS}}
- **Veri kapsamı:** {{DATA_COVERAGE}}

> Bu rapor yatırım, vergi veya hukuk tavsiyesi değildir. Skill hiçbir işlem, imza, onay veya köprüleme yapmaz.
