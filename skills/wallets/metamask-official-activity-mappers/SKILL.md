---
name: activity-mappers
description: >-
  Guidance for Activity List and Activity Item changes: start in
  `@metamask/client-utils/mappers` to share behavior across the mobile and
  extension apps. Prefer API data, or the keyring transaction for non-EVM;
  avoid massaging local state. Use when changing Activity List, Activity Item,
  or their data mapping.
---

# Activity mapper guide

## When to use

- Changing the Activity list, row, item, mapper, or a details template.
- Changing the Activity data, source precedence, filtering, or details routing.

## Workflow

1. Compare behavior with other MetaMask or wallet instances. If the issue is only in the local instance, look for any local-only implementation and try to revise/remove them. The preferred data source for EVM transactions is the Account Transactions API
2. Search closed Extension and Mobile issues and pull requests for similar Activity-related PRs.

3. Check whether `@metamask/client-utils` already maps the behavior.

4. For changes related to the Activity list, keep it within the mappers or selectors. For Activity Details, check the corresponding templates.
5. Add or update focused tests in the mapper, row, or details layer that owns the changed behavior.

## Start with the data source

| Source                             | Shared mapper           |
| ---------------------------------- | ----------------------- |
| EVM transaction                    | `mapApiTransaction`     |
| Non-EVM transaction                | `mapKeyringTransaction` |
| Ramps order                        | `mapRampsOrder`         |
| Pending and local-only transaction | `mapLocalTransaction`   |

## Extension and Mobile reference

| Feature, function, or flow                    | Mobile                                                                                                   | Extension                                                                                                                             |
| --------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Base Activity types and mappers               | `@metamask/client-utils` provides `ActivityItem` and core mappers                                        | `@metamask/client-utils` provides `ActivityItem` and core mappersts`                                                                  |
| API activity mapping                          | Mobile fetch hooks map API and domain sources into one Activity shape.                                   | `ui/pages/activity/useTransactionsQuery.ts` for lists. `mapApiTransaction` in `ui/pages/details/transaction-details.tsx` for details. |
| Non-EVM mapping                               | Mobile local adapters produce shared activity items for non-EVM sources.                                 | `mapKeyringTransaction` in `ui/selectors/activity.ts`.                                                                                |
| Local mapping                                 | `enrich-local-activity.ts` enriches core-mapper output with local facts.                                 | `selectLocalActivityItems` prepares mapper data. `ui/selectors/activity/enrich-local-activity.ts` adds Extension cases.               |
| Bridge and swap enrichment                    | Uses bridge quotes and legacy swap metadata to derive status and token legs.                             | Bridge history in `ui/selectors/activity.ts`.                                                                                         |
| Source merge and deduplication                | `adapters/dedup.ts` and list transformations prevent duplicate local, API, and domain rows.              | `ui/pages/activity/helpers.ts` deduplicates, sorts, and groups rows.                                                                  |
| Ramps mapping                                 | `ramp-order.ts` and `ramps-order.ts` handle two Mobile order sources.                                    | `ui/hooks/ramps/utils/mapRampsOrderSafely.ts` and `ui/selectors/rampsController/index.ts`.                                            |
| Predict activity                              | `predict-activity.ts` maps prediction, cash-out, and claim entries.                                      | No unified-list mapper or details template.                                                                                           |
| Fiat and token formatting                     | `fiat.ts` and `token-display.ts` format signed values and token amounts.                                 | `shared/lib/activity/fiat.ts` and `ui/pages/activity/rows/useActivityRowContent.tsx`.                                                 |
| List transformations                          | `activity-list-helpers.ts` handles date grouping, source precedence, and display data.                   | `ui/pages/activity/helpers.ts` and `ui/pages/activity/query-filters`.                                                                 |
| Activity list                                 | `ActivityList.tsx` and source hooks unify local, API, Perps, Predict, and Ramps items.                   | `ui/pages/activity/activity-list.tsx` unifies local, API, non-EVM, and Ramps items.                                                   |
| Activity rows                                 | `ActivityListItemRow.tsx`, layout, and icon helpers render rows.                                         | `ui/pages/activity/rows/activity-row.tsx`, `activity-row-layout.tsx`, and `useActivityRowContent.tsx`.                                |
| Pending rows and actions                      | Pending row and actions present queued and pending activity.                                             | `pending-activity-row.tsx` and `pending-transaction-actions.tsx`.                                                                     |
| Details item lookup                           | `useActivityDetailsItem.ts` resolves cached, API, local, and domain items.                               | `transaction-details.tsx` resolves Ramps, API or local EVM, non-EVM, then API.                                                        |
| Details template dispatch                     | `TemplateLoader.tsx` dispatches generic and domain-specific templates.                                   | `ui/pages/details/templates/template-loader.tsx`.                                                                                     |
| Details layout, amounts, status, and metadata | Mobile has reusable details frame, metadata, amount, fee, status, pending-banner, and footer components. | `ui/pages/details/components` plus templates.                                                                                         |

## Transaction details ownership

| Transaction details group                       | Detail files                                             | Domain team to involve        |
| ----------------------------------------------- | -------------------------------------------------------- | ----------------------------- |
| Shared mappers and generic Activity componentss | `pages/activity`, `pages/details`                        | `@MetaMask/core-extension-ux` |
| Swap and Bridge                                 | `pages/details/templates/bridge-details`                 | `@MetaMask/swaps-engineers`   |
| Perps                                           | `pages/details/templates/perps-details.tsx`              | `@MetaMask/perps`             |
| Money Account and MetaMask Pay                  | `money-account-details.tsx`, `mm-pay-details-layout.tsx` | `@MetaMask/earn`              |
| Ramps orders                                    | `ui/pages/details/templates/ramps`                       | `@MetaMask/money-movement`    |

##

##
