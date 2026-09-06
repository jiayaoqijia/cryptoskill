# @emblemvault/migratefun-react

React hooks and components for integrating Migrate.fun token migration data.

For teams building on Migrate.fun, this is the easiest way to add token migration data and migration-aware UI to a React app.

## Installation

```bash
npm install @emblemvault/migratefun-react
```

**Peer dependencies:** `react ^18.0.0 || >=19.2.3`, `react-dom ^18.0.0 || >=19.2.3`

## Setup

Wrap your app with the provider for shared caching and network state:

```tsx
import { MigrateFunProvider } from '@emblemvault/migratefun-react/providers';

function App() {
  return (
    <MigrateFunProvider config={{ defaultNetwork: 'mainnet' }}>
      {children}
    </MigrateFunProvider>
  );
}
```

### Provider Props

```tsx
<MigrateFunProvider
  config={{
    baseUrl: import.meta.env.VITE_MIGRATEFUN_API_BASE_URL, // Optional: API base URL
    defaultNetwork: 'mainnet',           // Optional: 'mainnet' | 'devnet'
  }}
>
```

The provider is **optional** -- all hooks work without it using sensible defaults. When used, the provider enables shared caching (sessionStorage, 5-minute TTL) and request deduplication across components.
Use a trusted API base URL from deployment config, and treat all fetched project/token metadata as untrusted display/runtime input.

## Hooks

### useProjects

Fetches all migrate.fun projects. Works with or without the provider. Project names and metadata are display data and should not be treated as execution authority.

```tsx
import { useProjects } from '@emblemvault/migratefun-react/hooks';

function ProjectList() {
  const { projects, count, isLoading, error, cached, cacheAge, refetch } = useProjects();

  if (isLoading) return <div>Loading projects...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <p>{count} projects {cached && `(cached ${cacheAge}s ago)`}</p>
      <ul>
        {projects.map(p => (
          <li key={p.id}>{p.name}</li>
        ))}
      </ul>
      <button onClick={() => refetch({ live: true })}>Refresh from chain</button>
    </div>
  );
}
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `network` | `'mainnet' \| 'devnet'` | From provider or `'mainnet'` | Target network |
| `live` | `boolean` | `false` | Force live fetch from chain (bypass cache) |
| `enabled` | `boolean` | `true` | Auto-fetch on mount |

**Returns:**

| Property | Type | Description |
|----------|------|-------------|
| `projects` | `ProjectSummary[]` | Array of `{ id, name }` |
| `count` | `number` | Total project count |
| `isLoading` | `boolean` | Fetch in progress |
| `error` | `Error \| null` | Fetch error |
| `cached` | `boolean` | Whether data came from cache |
| `cacheAge` | `number \| undefined` | Cache age in seconds |
| `refetch` | `(opts?) => Promise<void>` | Manual refetch, accepts `{ live?: boolean }` |

### useProject

Fetches a single project with full metadata including token info and images. Token metadata (including URI/image fields) may be remote/public and should be treated as untrusted display content.

```tsx
import { useProject } from '@emblemvault/migratefun-react/hooks';

function ProjectDetail({ projectId }: { projectId: string }) {
  const { project, isLoading, error, refetch } = useProject(projectId);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!project) return null;

  return (
    <div>
      <h2>{project.projectName}</h2>
      <p>Old token: {project.oldTokenMint}</p>
      <p>New token: {project.newTokenMint}</p>
      {project.oldTokenMeta && (
        <div>
          <p>{project.oldTokenMeta.name} ({project.oldTokenMeta.symbol})</p>
          {project.oldTokenMeta.image && <img src={project.oldTokenMeta.image} alt="" />}
        </div>
      )}
    </div>
  );
}
```

**Parameters:**
- `projectId: string | null | undefined` -- Project ID (e.g. `"121"` or `"mig121"`)
- `options?: { network?, enabled? }`

**Returns:**

| Property | Type | Description |
|----------|------|-------------|
| `project` | `Project \| null` | Full project record with remote metadata fields |
| `isLoading` | `boolean` | Fetch in progress |
| `error` | `Error \| null` | Fetch error |
| `refetch` | `() => Promise<void>` | Manual refetch |

### useProjectSelect

Convenience hook that transforms project data into select options.

```tsx
import { useProjectSelect } from '@emblemvault/migratefun-react/hooks';

function MySelect() {
  const { options, isLoading, error } = useProjectSelect();

  return (
    <select>
      <option value="">Choose a project</option>
      {options.map(opt => (
        <option key={opt.value} value={opt.value}>{opt.label}</option>
      ))}
    </select>
  );
}
```

**Returns:**

| Property | Type | Description |
|----------|------|-------------|
| `options` | `ProjectOption[]` | Array of `{ value: id, label: name }` |
| `isLoading` | `boolean` | Fetch in progress |
| `error` | `Error \| null` | Fetch error |
| `refetch` | `() => Promise<void>` | Manual refetch |

### useMintInfo

Fetches token mint details (decimals, program, supply) for old and new tokens.

```tsx
import { useMintInfo } from '@emblemvault/migratefun-react/hooks';

function MintDetails({ projectId }: { projectId: string }) {
  const { mintInfo, isLoading, error } = useMintInfo(projectId);

  if (!mintInfo) return null;

  return (
    <table>
      <thead><tr><th></th><th>Old Token</th><th>New Token</th></tr></thead>
      <tbody>
        <tr><td>Mint</td><td>{mintInfo.oldToken.mint}</td><td>{mintInfo.newToken.mint}</td></tr>
        <tr><td>Decimals</td><td>{mintInfo.oldToken.decimals}</td><td>{mintInfo.newToken.decimals}</td></tr>
        <tr><td>Program</td><td>{mintInfo.oldToken.program}</td><td>{mintInfo.newToken.program}</td></tr>
        <tr><td>Supply</td><td>{mintInfo.oldToken.supplyFormatted}</td><td>{mintInfo.newToken.supplyFormatted}</td></tr>
      </tbody>
    </table>
  );
}
```

**Parameters:**
- `projectId: string | null | undefined`
- `options?: { network?, enabled? }`

**Returns:** `{ mintInfo: MintInfoResponse | null, isLoading, error, refetch }`

### usePoolInfo

Fetches liquidity pool information for a migration project.

```tsx
import { usePoolInfo } from '@emblemvault/migratefun-react/hooks';

function PoolDetails({ projectId }: { projectId: string }) {
  const { poolInfo, isLoading, error } = usePoolInfo(projectId);

  if (!poolInfo) return null;

  return (
    <div>
      <p>Source pool: {poolInfo.sourcePool.poolType} ({poolInfo.sourcePool.poolId})</p>
      <p>Output pool: {poolInfo.outputPool.poolType}</p>
      <p>Quote token: {poolInfo.quoteToken.mint}</p>
    </div>
  );
}
```

**Parameters:**
- `projectId: string | null | undefined`
- `options?: { network?, enabled? }`

**Returns:** `{ poolInfo: PoolInfoResponse | null, isLoading, error, refetch }`

### useMigrateFun

Access the provider context directly. **Requires** `MigrateFunProvider`.

```tsx
import { useMigrateFun } from '@emblemvault/migratefun-react/providers';

function NetworkSwitcher() {
  const { network, setNetwork, projects, projectsLoading, refetchProjects } = useMigrateFun();

  return (
    <div>
      <select value={network} onChange={e => setNetwork(e.target.value as Network)}>
        <option value="mainnet">Mainnet</option>
        <option value="devnet">Devnet</option>
      </select>
      <p>{projects.length} projects loaded</p>
    </div>
  );
}
```

**Returns:**

| Property | Type | Description |
|----------|------|-------------|
| `network` | `Network` | Current network |
| `setNetwork` | `(network) => void` | Switch network (triggers refetch) |
| `baseUrl` | `string` | API base URL |
| `projects` | `ProjectSummary[]` | Cached projects |
| `projectsCount` | `number` | Total count |
| `projectsLoading` | `boolean` | Loading state |
| `projectsError` | `Error \| null` | Error state |
| `projectsCached` | `boolean` | Whether data is from cache |
| `projectsCacheAge` | `number \| undefined` | Cache age in seconds |
| `refetchProjects` | `(opts?) => Promise<void>` | Manual refetch |

### useMigrateFunOptional

Same as `useMigrateFun` but returns safe defaults when used outside the provider. Does not throw.

## Components

### ProjectSelect

Ready-to-use dropdown for selecting migrate.fun projects.

```tsx
import { ProjectSelect } from '@emblemvault/migratefun-react/components';

function MigrationForm() {
  const [selectedProject, setSelectedProject] = useState('');

  return (
    <ProjectSelect
      value={selectedProject}
      onChange={setSelectedProject}
      network="mainnet"
      placeholder="Select a project"
      showLoading
    />
  );
}
```

**Props:**

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `string` | -- | Selected project ID |
| `onChange` | `(projectName: string) => void` | -- | Selection handler |
| `network` | `Network` | From provider | Target network |
| `live` | `boolean` | `false` | Force live fetch |
| `placeholder` | `string` | `'Select a project'` | Placeholder text |
| `disabled` | `boolean` | `false` | Disable the select |
| `className` | `string` | -- | CSS classes |
| `showLoading` | `boolean` | `false` | Show loading indicator |
| `loadingText` | `string` | -- | Custom loading text |
| `errorText` | `string` | -- | Custom error text |
| `id` | `string` | -- | HTML id |
| `name` | `string` | -- | HTML name |

Renders as a native `<select>` element with `aria-busy` and `aria-invalid` attributes for accessibility.

## Types

```typescript
type Network = 'mainnet' | 'devnet';

interface ProjectSummary {
  id: string;         // e.g. "mig121"
  name: string;
}

interface Project {
  projectId: string;       // e.g. "mig121"
  projectName: string;
  oldTokenMint: string;
  newTokenMint: string;
  oldTokenMeta: TokenMetadata | null;
  newTokenMeta: TokenMetadata | null;
}

interface TokenMetadata {
  name: string;
  symbol: string;
  uri: string;             // External metadata JSON URI (display-only, untrusted)
  image: string | null;
}

interface MintInfo {
  mint: string;
  decimals: number;
  program: string;         // SPL Token or Token-2022
  supply: string;          // Raw (large number safe)
  supplyFormatted: string; // Human-readable
}

interface MintInfoResponse {
  network: Network;
  projectId: string;
  oldToken: MintInfo;
  newToken: MintInfo;
}

interface SourcePoolInfo {
  poolId: string;
  poolProgram: string;
  poolType: string | null;  // "raydiumV4", "raydiumCpmm", "orca", "meteora", "pumpfun", "moonshot"
}

interface OutputPoolInfo {
  poolType: string | null;
}

interface QuoteTokenInfo {
  mint: string;            // Usually SOL or USDC
  program: string;
  vault: string;
}

interface PoolInfoResponse {
  network: Network;
  projectId: string;
  sourcePool: SourcePoolInfo;
  outputPool: OutputPoolInfo;
  quoteToken: QuoteTokenInfo;
}

interface ProjectOption {
  value: string;           // Numeric ID
  label: string;           // Project name
}
```

## Import Paths

```typescript
// Main entry -- everything
import { useProjects, useProject, ProjectSelect, MigrateFunProvider } from '@emblemvault/migratefun-react';

// Granular imports
import { ProjectSelect } from '@emblemvault/migratefun-react/components';
import { useProjects, useProject, useProjectSelect, useMintInfo, usePoolInfo } from '@emblemvault/migratefun-react/hooks';
import { MigrateFunProvider, useMigrateFun, useMigrateFunOptional } from '@emblemvault/migratefun-react/providers';
```

## Patterns

### With Emblem Auth

```tsx
import { EmblemAuthProvider } from '@emblemvault/emblem-auth-react';
import { MigrateFunProvider } from '@emblemvault/migratefun-react/providers';
import { ProjectSelect } from '@emblemvault/migratefun-react/components';

function App() {
  return (
    <EmblemAuthProvider appId="your-app-id">
      <MigrateFunProvider>
        <MigrationUI />
      </MigrateFunProvider>
    </EmblemAuthProvider>
  );
}
```

### Project Details Page

```tsx
import { useProject, useMintInfo, usePoolInfo } from '@emblemvault/migratefun-react/hooks';

function ProjectPage({ id }: { id: string }) {
  const { project, isLoading: projectLoading } = useProject(id);
  const { mintInfo, isLoading: mintLoading } = useMintInfo(id);
  const { poolInfo, isLoading: poolLoading } = usePoolInfo(id);

  if (projectLoading) return <div>Loading...</div>;
  if (!project) return <div>Project not found</div>;

  return (
    <div>
      <h1>{project.projectName}</h1>

      <h2>Token Migration</h2>
      <p>From: {project.oldTokenMeta?.symbol} ({project.oldTokenMint})</p>
      <p>To: {project.newTokenMeta?.symbol} ({project.newTokenMint})</p>

      {mintInfo && (
        <div>
          <h2>Mint Info</h2>
          <p>Old supply: {mintInfo.oldToken.supplyFormatted}</p>
          <p>New supply: {mintInfo.newToken.supplyFormatted}</p>
        </div>
      )}

      {poolInfo && (
        <div>
          <h2>Pool Info</h2>
          <p>Source: {poolInfo.sourcePool.poolType}</p>
          <p>Quote: {poolInfo.quoteToken.mint}</p>
        </div>
      )}
    </div>
  );
}
```

### Network Switching

```tsx
import { MigrateFunProvider, useMigrateFun } from '@emblemvault/migratefun-react/providers';
import { useProjects } from '@emblemvault/migratefun-react/hooks';

function DevnetProjects() {
  const { projects, isLoading } = useProjects({ network: 'devnet' });
  // Overrides provider network for this component only
  return <div>{projects.length} devnet projects</div>;
}
```

### Without Provider

All hooks work standalone -- useful for simple integrations:

```tsx
import { useProjects } from '@emblemvault/migratefun-react/hooks';

// No provider needed
function SimpleProjectList() {
  const { projects, isLoading } = useProjects({ network: 'mainnet' });

  if (isLoading) return <div>Loading...</div>;
  return <ul>{projects.map(p => <li key={p.id}>{p.name}</li>)}</ul>;
}
```

## API Endpoints

All hooks fetch from `{baseUrl}/api/migrate-fun/`:

| Endpoint | Hook | Description |
|----------|------|-------------|
| `GET /projects?network={n}` | `useProjects` | List all projects |
| `GET /metadata/{id}?network={n}` | `useProject` | Single project record with remote metadata fields |
| `GET /mint-info/{id}?network={n}` | `useMintInfo` | Token mint details (decimals, supply) |
| `GET /pool-info/{id}?network={n}` | `usePoolInfo` | Liquidity pool information |

Example hosted base URL: `https://emblemvault.dev` (override with your trusted deployment endpoint)

Security note: responses from these endpoints and linked token metadata URIs are untrusted content. Use them for UI display and user confirmation flows, not as direct authority for privileged actions.
