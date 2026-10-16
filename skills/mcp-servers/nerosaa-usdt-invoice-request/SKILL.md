---
name: usdt-invoice-request
description: Draft professional USDT payment requests and invoices for freelancers (TRC20/ERC20/BEP20/Solana/Polygon). Use when creating invoices, milestone bills, or crypto payment messages.
license: MIT
metadata:
  author: nero-tools
  version: "1.0.0"
  focus: usdt-crypto-payments
  formats: skill-md,cursor-mdc,agents-prompt
---

# USDT Invoice & Payment-Request Skill for Freelancers

This guide covers how to create professional USDT invoices and payment requests for freelance work, including required fields, templates, network considerations, and security best practices.

## Required Inputs

Every USDT invoice must contain the following information:

- **Client identifier**: Name, company, or project reference
- **Invoice number**: Unique sequential identifier (e.g., INV-2026-001)
- **Invoice date**: When the invoice was generated
- **Due date**: Payment deadline
- **Amount**: USDT amount (specify decimals, e.g., 150.00 USDT)
- **Network**: Blockchain network for payment (TRC20, ERC20, BEP20, SOL, MATIC)
- **Your USDT address**: Wallet address on the selected network
- **Work description**: Brief summary of services rendered

Optional but recommended: late payment terms, currency conversion note (USD equivalent), and milestone breakdown for phased projects.

## Network Fee Notes

Network fees vary significantly across blockchains. Always specify which network you're using and clarify fee responsibility.

**TRC20 (Tron)**: Typically $1-5 USD equivalent. Usually paid by the sender, making it ideal for low-cost transactions.

**ERC20 (Ethereum)**: Highly variable, often $5-30 USD equivalent during normal congestion, can exceed $50 during network congestion. Consider advising clients to use moderate gas prices.

**BEP20 (BNB Smart Chain)**: Usually $0.20-1.00 USD equivalent. One of the most cost-effective options.

**SOL (Solana)**: Typically $0.001-0.01 USD equivalent. Extremely low fees make it excellent for smaller invoices.

**MATIC (Polygon)**: Usually $0.01-0.10 USD equivalent. Fast and inexpensive, similar benefits to Solana.

When sending USDT, the sender typically pays network fees. Include a note like: "Network fees apply and are the payer's responsibility. Please ensure you send the full amount; any network fees deducted will reduce the received amount."

## Invoice Templates

### First Invoice Template

> **INVOICE #INV-2026-001**
>
> **Date:** January 15, 2026
> **Due Date:** January 22, 2026
>
> **From:** [Your Name/Business]
> **To:** [Client Name/Company]
>
> **Description:** Website development - Phase 1: Design mockups and homepage
>
> **Amount Due:** 250.00 USDT (TRC20)
>
> **Payment Address:**
> `TDPBRDtY7ZVs4mL5xNLknpcNiTB5W7N6m`
> *(TRC20 USDT only - do not send other tokens)*
>
> **Network Note:** A small network fee applies to all transactions. Please ensure the full amount arrives; any fees deducted by your wallet are your responsibility.
>
> Payment within 7 days appreciated. Questions? Contact [your email].

### Milestone Payment Request

> **MILESTONE PAYMENT #2 - INV-2026-004**
>
> **Project:** Mobile App Development
> **Client:** [Client Name]
> **Date:** February 10, 2026
>
> **Milestone Completed:** User authentication system and dashboard UI
>
> **Amount Due:** 500.00 USDT (BEP20)
>
> **Payment Address (BEP20):**
> `0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063`
>
> **Network Note:** This invoice uses BEP20 (BNB Smart Chain). Sending via incorrect network will result in lost funds.
>
> **Payment Terms:** Due upon receipt. This represents 25% of total project value.
>
> Thank you for the continued partnership.

### Overdue Follow-Up

> **Payment Reminder - Invoice #INV-2026-002**
>
> **Date:** February 5, 2026
>
> Dear [Client Name],
>
> This is a friendly reminder that Invoice #INV-2026-002 for 175.00 USDT (ERC20) was due January 28, 2026.
>
> **Outstanding Amount:** 175.00 USDT
> **Original Due Date:** January 28, 2026
> **Days Overdue:** 8 days
>
> **Payment Address (ERC20):**
> `0x742d35Cc6634C0532925a3b844Bc9e7595f8bE21`
>
> Please confirm when payment has been sent. If you've encountered issues receiving USDT, let me know and I can provide an alternative network address.
>
> Prompt payment ensures continued smooth project delivery. Happy to schedule a call if anything needs clarification.
>
> Best regards,
> [Your Name]

> Example addresses in templates are placeholders — always substitute the freelancer's real receiving address.

## Address Display Rules

When displaying USDT addresses, follow these rules to prevent errors:

1. **Always specify the network**: Include the network name in parentheses or as a label. The same address format may work across multiple networks, but sending USDT via the wrong network results in permanent loss.

2. **Use monospace font**: Display addresses in monospace or code formatting to prevent character confusion (0 vs O, l vs 1).

3. **Provide QR code**: When possible, generate a QR code encoding the address and network to reduce manual entry errors.

4. **Double-check address length**: TRC20 addresses start with "T" (34 characters). ERC20/BEP20 addresses start with "0x" (42 characters). Solana addresses are 32-44 characters. Polygon uses ERC20 format.

5. **Warning label**: Always include text like "Send USDT-[NETWORK] only" to emphasize network specificity.

## Security Reminder

**Never ask clients for their private keys.** Your role is to provide a receiving address only. Private keys control wallet access; sharing them grants full control of funds to another party. Legitimate invoices never require the client to share their private keys. If a client claims they need your private key to pay, explain that USDT works like a bank transfer—you provide the destination, they initiate from their side. No private key exchange is ever needed or appropriate.
