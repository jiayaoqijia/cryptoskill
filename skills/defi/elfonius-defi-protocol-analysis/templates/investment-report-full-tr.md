<!-- İÇ NOT: 8–15 sayfalık derin DeFi raporu. Her alanı doldur; bu yorumu, boş satırları ve kullanılmayan bölümleri teslimattan önce sil. references/report-production.md ile birlikte kullan. Yönetici özeti zorunlu. -->

# {{Protokol / vault}} — DeFi Yatırım Araştırması

**Tarih (UTC):** {{gg.aa.yyyy ss:dd}} · **Karar:** {{mevduat | al | elde tut | çık | karşılaştır}}
**Zincir / tam kontrat / ürün:** {{...}} · **Token:** {{...}}
**Hazırlayan:** {{isim}} · **Veri as-of:** {{tarih}}

## Kapak

- Başlık: {{protokol}} — {{tek cümlelik tez}}
- Alt başlık: {{gerçek getiri, zayıf token | iyi ürün, kötü çıkış | ...}}
- Hüküm: {{uygun | izle | kaçın | kanıt yetersiz}}
- Dört metrik: {{TVL}} · {{yıllık ücret}} · {{yıllık gelir}} · {{piyasa değeri / FDV}}
- İçindekiler: {{01 Kimlik · 02 Yığın · ...}}

## Yönetici Özeti — 1 sayfa

{{Dört kısa paragraf: ürün ne, kullanıcı neyi sahipleniyor, neden şimdi, hüküm. Sonra değerlendirme matrisi ve "ne izlenmeli".}}

| Boyut | Durum | Kısa kanıt |
|---|---|---|
| Tam deployment | | |
| Ürün / mekanizma | | |
| Pazar / rekabet | | |
| Kullanım / talep | | |
| Ücret / gelir | | |
| Token / değer yakalama | | |
| Likidite / çıkış | | |
| Teminat / oracle | | |
| Güvenlik / denetim | | |
| Admin / yönetişim | | |
| Hukuk / uygunluk | | |

**Ne izlenmeli:** {{4 madde}} · **Raporun sınırı:** {{yapılmayan kontroller}}

## 01 · Karar çerçevesi ve tam hedef

{{Karar, ufuk, numeraire, benchmark, jurisdiction, azami kayıp, likidite, mevcut maruziyet. Zincir, sürüm, ürün, tam kontrat, proxy/implementation, token, hukuki entity. İsim çakışmaları/forks/köprü versiyonları; blok ve UTC.}}

## 02 · Tam yığın ve mekanizma

{{Beş katman: venue, vault/küratör, alttaki varlıklar/karşı taraflar, oracle/köprü/keeper, ön uç. Kim ödüyor, wrapper ne ekliyor, nakit akışı nerede doğuyor. Yığın tablosu/şeması.}}

## 03 · Ürün ve gerçek kullanım

{{Müşteri problemi, ürün, fiyat, dağıtım, elde tutma, aktif kullanıcı, hacim, utilization, konsantrasyon. Ücretli/teşvikli, dış/grup içi. Kanıt: protokol API, dashboard, zincir.}}

## 04 · Pazar ve rekabet

{{Bottom-up pazar, 3–5 peer, pay, ücret/faiz/latency/zincir dağılımı, likidite ağ etkisi, geçiş maliyeti, moat, fork/fiyat savaşı. Grafik: pazar payı veya TVL/hacim.}}

## 05 · Ücretler, gelir ve birim ekonomisi

{{Aktivite → brüt ücret → tedarikçi geliri → protokol geliri → token sahibi geliri → teşvik sonrası kazanç. Birim gelir/maliyet, marj, teşvik yoğunluğu, hazine runway'i. Tablo + stres testi.}}

## 06 · Token ve değer yakalama

{{Haklar merdiveni, arz köprüsü, float/FDV, emisyon/kilit açılımı, insider/VC dağılımı, geri alım/yakım finansmanı, token'ın kendi teminatı olması, yönetişim. Tablo.}}

## 07 · Likidite, çıkış, uygulama ve stres

{{Büyüklük bazında derinlik, slippage, kuyruk/cooldown, cap, utilization, köprü gecikmesi, CEX/DEX, kilitler, gerçekleşen çıkış maliyeti. Cüzdan türü, resmi domain/kontrat, calldata/spender/allowance, simülasyon, RPC/MEV koruması ve unwind yolu. %25/50/100 çıkış stresi. Grafik: çıkış maliyeti/büyüklük.}}

## 08 · Teminat, kredi ve likidasyon

{{LTV/LLTV, likidasyon eşiği/bonusu/close factor, oracle, keeper teşviki, bad debt, isolation/eMode, rekürsif teminat, rehypothecation, stablecoin depeg. Gerçekçi gas/derinlikte likidasyon yolu.}}

## 09 · Güvenlik ve denetimler

{{Kaynak/bytecode eşleşmesi, denetim kapsamı/tarihi/commit'i/bulguları/düzeltmesi, formal verification, bug bounty, olay geçmişi, admin/upgrade/pause, multisig/timelock. Tablo.}}

## 10 · Ekip, yönetişim, hukuk ve regülasyon

{{Kurucular, doğrulanmış geçmiş, fonlama, key-person, çıkar çatışmaları ve katkıcı konsantrasyonu. Token dağılımı/delegeler/quorum, teklif geçmişi, hazine kontrolü ve acil yetkiler. Entity, jurisdiction, MiCA/menkul kıymet/yaptırım/KYC-AML, saklama, vergi, sigorta/risk transferi; hukukçu uyarısı.}}

## 11 · Bağımlılıklar ve sistemik risk

{{Köprüler, oracle'lar, stablecoin'ler, LST/LRT, RWA wrapper, küratör, keeper, zincir/RPC. Korelasyon, bulaşma, çift sayım, kompoze pozisyonlar. Küme haritası.}}

## 12 · Piyasa yapısı, teknik ve topluluk

{{Fiyat/hacim, funding/basis, volatilite, drawdown, relatif güç, derinlik; sosyal/GitHub/yönetişim/haber/katalizör. Sentiment sinyaldir. Teknik yalnızca zamanlama için.}}

## 13 · Değerleme

{{Yöntem ve gerekçesi; P/F, P/S, P/E veya senaryo aralığı; ters değerleme; ücret payı düzeltmesi; beklenen getiri ve tam kayıp dalı. Grafik: değerleme aralığı.}}

| Senaryo | Ana varsayım | Değer / getiri | Cariye göre |
|---|---|---:|---:|
| Bear | | | |
| Base | | | |
| Bull | | | |

## 14 · Risk, stres ve portföy uygunluğu

{{Risk matrisi (olasılık/etki), tail senaryolar, korelasyon, drawdown, likidite, jurisdiction, küme maruziyeti. Kompozit skor yok. Uygunluk yalnızca kısıtlar verilirse.}}

## 15 · Karar ve izleme

{{Kapı, koşullu hüküm, 2–3 falsifier, izleme panosu (metrik, cari, eşik, kaynak, sıklık), neyin pozisyonu küçülteceği.}}

## Kaynaklar ve metodoloji

{{Numaralı kaynaklar, as-of tarihleri, tanımlar (TVL, ücret, gelir, token sahibi geliri, FDV), veri çelişkileri, kanıt sınıfları, kapsam dışı.}}
