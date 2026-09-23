# Agentic Testability (testIDs)

PRs that touch UI components must include testIDs so agentic recipes and E2E tests can navigate and assert on the app without manual interaction.

- **Missing testID on interactive elements** — any `TextInput`, `Pressable`, `Button`, or touchable in a new or modified component without a `testID` prop. Agentic recipes use `app-state.sh press <testID>` and `eval_sync` fiber-walk queries to interact with and assert on UI. If the element has no testID, the recipe cannot press it or read its value — the fix is untestable agentically.
- **testID not in `Perps.testIds.ts`** — testIDs defined as inline strings instead of exported constants from `app/components/UI/Perps/Perps.testIds.ts`. All testIDs must be centralized so recipes can reference them by constant name.
- **testID missing from the element that holds the value** — adding testID to a wrapper View instead of the `TextInput` or Text that actually contains the value. CDP fiber-walk reads `value` from the React element with the matching testID — the testID must be on the element that owns the state.
- **TP/SL price inputs without testID** — the trigger price `TextInput` components in `PerpsTPSLView` (and similar order-form screens) frequently lack testIDs, making it impossible to assert the accepted decimal precision agentically. Any PR touching these screens must add `testID` to both the Take Profit and Stop Loss price inputs.
