# Component structure examples

Synthetic snippets, one before/after per rule. Each shows only the lines the rule changes. Copy and navigation calls use neutral names (`t`, `navigate`); see the repo overlay for the Mobile (`strings()`, React Navigation) or Extension (`useI18nContext()`, `react-router-dom` v6) API. All snippets are React 18-safe.

Target layout for a screen that follows R1 and R3:

```text
<Screen>/
  <Screen>.tsx          # composition only: reads use<Screen>, renders JSX
  use<Screen>.ts        # state, async flows, handlers; returns { state, actions }
  use<Screen>.test.ts
  components/
    <SubComponent>/
      <SubComponent>.tsx
      <SubComponent>.test.tsx
```

## R1 — One component per file

```tsx
// Before: Row is a new type each render, so it remounts and loses state.
const Settings = ({ items }: Props) => {
  const Row = ({ item }: { item: Item }) => <ListItem label={item.label} />;
  const renderFooter = () => <Footer onSave={save} />;
  return (
    <>
      {items.map((item) => <Row key={item.id} item={item} />)}
      {renderFooter()}
    </>
  );
};

// After: Settings/components/SettingsRow/SettingsRow.tsx
export const SettingsRow = ({ item }: SettingsRowProps) => (
  <ListItem label={item.label} />
);

// Settings/Settings.tsx
const Settings = ({ items }: Props) => (
  <>
    {items.map((item) => <SettingsRow key={item.id} item={item} />)}
    <Footer onSave={save} />
  </>
);
```

## R2 — Fixed body order

```tsx
// Before: derived values after the early return and after handlers.
const Form = () => {
  const [value, setValue] = useState('');
  const onSubmit = () => submit(value);
  const account = useSelector(selectAccount);
  if (!account) return null;
  const isValid = value.length > 0;
  return <Button disabled={!isValid} onPress={onSubmit} />;
};

// After: selectors, state, derived, handlers, early return, JSX.
const Form = () => {
  const account = useSelector(selectAccount);
  const [value, setValue] = useState('');
  const isValid = value.length > 0;
  const onSubmit = () => submit(value);
  if (!account) return null;
  return <Button disabled={!isValid} onPress={onSubmit} />;
};
```

## R3 — The component is composition

```tsx
// Before: vault, analytics and navigation in the component body.
const onConfirm = async () => {
  try {
    setStatus('submitting');
    await createVault(password);
    trackEvent('VaultCreated');
    navigate('Success');
  } catch (error) {
    setStatus('failed');
    trackEvent('VaultFailed', { error: String(error) });
  }
};

// After: useCreateVault.ts owns the flow and returns { state, actions }.
export const useCreateVault = () => {
  const [status, setStatus] = useState<Status>('idle');
  const confirm = async (password: string) => { /* same flow */ };
  return { state: { status }, actions: { confirm } };
};

// CreateVault.tsx only composes.
const { state, actions } = useCreateVault();
return <Button loading={state.status === 'submitting'} onPress={() => actions.confirm(password)} />;
```

## R4 — `useEffect` only for external sync

```tsx
// Before: async fetch with a hand-rolled cancelled flag.
const [metadata, setMetadata] = useState<Metadata>();
const [isLoading, setIsLoading] = useState(false);
useEffect(() => {
  let cancelled = false;
  const load = async () => {
    setIsLoading(true);
    const result = await fetchMetadata(address);
    if (!cancelled) {
      setMetadata(result);
      setIsLoading(false);
    }
  };
  load();
  return () => {
    cancelled = true;
  };
}, [address]);

// After: TanStack Query owns caching, cancellation and loading state.
const { data: metadata, isLoading } = useQuery({
  queryKey: ['tokenMetadata', chainId, address],
  queryFn: () => fetchMetadata(address),
  enabled: Boolean(address),
});
```

Effect that mirrors a prop into state, and the fix:

```tsx
// Before
useEffect(() => { setForm(emptyForm); }, [chainId]);
// After: remount the form when chainId changes.
<TokenForm key={chainId} />
```

## R5 — Mutually exclusive phases are one state

```tsx
// Before: isLoading && isReady is representable.
const [isLoading, setIsLoading] = useState(true);
const [isReady, setIsReady] = useState(false);
const [error, setError] = useState<string>();

// After: one union, phase data on its variant.
type Status =
  | { kind: 'loading' }
  | { kind: 'ready' }
  | { kind: 'failed'; error: string };
const [status, setStatus] = useState<Status>({ kind: 'loading' });

switch (status.kind) {
  case 'loading':
    return <Spinner />;
  case 'failed':
    return <ErrorBanner message={status.error} />;
  case 'ready':
    return <Content />;
}
```

## R6 — Values set together move to a reducer

```tsx
// Before: the same three setters in two handlers.
const onClear = () => { setInput(''); setAddress(undefined); setDomain(undefined); };
const onChainChange = () => { setInput(''); setAddress(undefined); setDomain(undefined); };

// After: one action per transition.
type Action = { type: 'reset' } | { type: 'resolved'; address: string; domain: string };
const reducer = (state: FormState, action: Action): FormState => {
  switch (action.type) {
    case 'reset':
      return initialFormState;
    case 'resolved':
      return { ...state, address: action.address, domain: action.domain };
  }
};
const [form, dispatch] = useReducer(reducer, initialFormState);
const onClear = () => dispatch({ type: 'reset' });
```

## R7 — No reflexive manual memoization under React Compiler

```tsx
// Before: memoization the compiler already provides.
const isTooShort = useCallback(() => password.length < MIN_LENGTH, [password]);
const label = useMemo(() => `${name} (${symbol})`, [name, symbol]);
const onPress = useCallback(() => setOpen(true), []);

// After
const isTooShort = password.length < MIN_LENGTH;
const label = `${name} (${symbol})`;
const onPress = () => setOpen(true);
```

Kept, because an API needs stable identity:

```tsx
// Mobile: React Navigation focus effect.
useFocusEffect(useCallback(() => refresh(), [refresh]));
// Both repos: a debounced function must survive renders.
const debouncedValidate = useMemo(() => debounce(validate, 500), [validate]);
```

## R9 — Subscribe where the value is used

```tsx
// Before: every price tick re-runs the whole screen body.
const OrderScreen = ({ symbol }: Props) => {
  const price = useLivePrice(symbol);
  const form = useOrderForm();
  // ...many hooks, derived values and handlers
  return (
    <>
      <PriceHeader price={price} />
      <OrderForm form={form} />
    </>
  );
};

// After: only the header re-renders on a tick.
// OrderScreen/components/PriceHeader/PriceHeader.tsx
export const PriceHeader = ({ symbol }: PriceHeaderProps) => {
  const price = useLivePrice(symbol);
  return <Text>{formatPrice(price)}</Text>;
};

// OrderScreen/OrderScreen.tsx
const OrderScreen = ({ symbol }: Props) => {
  const form = useOrderForm();
  return (
    <>
      <PriceHeader symbol={symbol} />
      <OrderForm form={form} />
    </>
  );
};
```

List row:

```tsx
// Before: each row re-renders when any rate changes.
const TokenRow = ({ token }: Props) => {
  const rates = useSelector(selectAllRates);
  const fiat = token.balance * (rates[token.id]?.price ?? 0);
  return <ListItem label={token.symbol} value={fiat} />;
};

// After: the row reads only its own rate (a primitive).
const TokenRow = ({ token }: Props) => {
  const price = useSelector((state) => selectRateById(state, token.id));
  return <ListItem label={token.symbol} value={token.balance * (price ?? 0)} />;
};
```
