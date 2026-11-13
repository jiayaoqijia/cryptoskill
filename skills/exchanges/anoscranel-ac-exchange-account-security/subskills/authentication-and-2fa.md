---
name: authentication-and-2fa
domain: crypto-trading/authentication-and-2fa
trigger: "Choosing and reviewing login factors and session controls."
anti_trigger: "Not for handling credentials, and not for venue selection."
scope: "Second factors, hardware keys, session and device control, and the weakest link in each."
status: seedling
---

# Authentication and 2FA

## Standard

Second factors are not equal. A code generated on a device the attacker does not control resists phishing better than a code sent by message, and a hardware key resists it better still, because the key verifies the domain it is talking to. The ranking is not a matter of preference: it follows from what each factor requires the attacker to possess or to fake.

Sessions are the other half. A factor protects the login; session controls decide how long a login lasts, whether a new device must be approved, and whether an active session can be seen and revoked. A strong factor with unlimited session life still leaves a stolen session as a live threat, which is why session review belongs in the same procedure.

Primary sources: <https://www.nist.gov/> and <https://www.cisa.gov/>.

## Decision rules

- The strongest available factor is enabled: hardware key first, then an authenticator app, then message-based codes.
- Message-based factors are recorded as a weakness, not as an equivalent control.
- Session lifetime is set to the shortest workable period, and active sessions are reviewed.
- New-device approval is enabled where offered.
- Recovery codes are stored offline and recorded as existing, never as values.
- Any factor change is followed by a review of sessions and keys.

## Procedure

1. Record the factors available at each venue.
2. Enable the strongest factor and register a backup factor.
3. Set session lifetime and device approval.
4. Review and revoke unknown active sessions.
5. Store recovery material offline and record its location.
6. Record the configuration and its weak points.

## Anti-patterns

- Using message-based codes because they are the default.
- Registering a single factor with no backup.
- Leaving sessions open indefinitely on shared devices.
- Storing recovery codes in the same password manager as the password.
- Assuming a factor change closes existing sessions.

## Done checklist

- [ ] Available factors recorded per venue.
- [ ] Strongest factor enabled with a backup.
- [ ] Session lifetime and device approval set.
- [ ] Active sessions reviewed.
- [ ] Recovery material stored offline and located in the record.
- [ ] Weak points recorded.

The practical test is the recovery scenario: if the primary device is lost today, can the account be reached, and by whom? An account that cannot be recovered is a control that has become a risk, and one that can be recovered by anyone who knows the answers to a few questions is not protected at all.

## Sources

- Digital identity and authenticator guidance: <https://www.nist.gov/>
- Cybersecurity guidance for accounts and access: <https://www.cisa.gov/>
- Market-participant security guidance: <https://www.sec.gov/investor>
