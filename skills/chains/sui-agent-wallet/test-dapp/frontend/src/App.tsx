import { useState, useEffect } from 'react';
import {
  ConnectButton,
  useCurrentAccount,
  useSignAndExecuteTransaction,
} from '@mysten/dapp-kit';
import { Transaction } from '@mysten/sui/transactions';
import { SuiClient, getFullnodeUrl } from '@mysten/sui/client';

// Create a standalone client for fetching (doesn't depend on wallet connection)
const suiClient = new SuiClient({ url: getFullnodeUrl('testnet') });

// Deployed on testnet (via Agent Wallet!)
const PACKAGE_ID = '0x4844d085e9ead209a33b4cae64db0b6a774dd2132955803234ae1e07211aac53';
const COUNTER_ID = '0x09f156cd082bbb8d88bbe67fe80d905b619e91bd905a2ef29d69862706bd1e16';

export default function App() {
  const account = useCurrentAccount();
  const { mutate: signAndExecute, isPending } = useSignAndExecuteTransaction();
  
  const [counterValue, setCounterValue] = useState<number | null>(null);
  const [status, setStatus] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);

  // Fetch counter value (uses standalone client, works without wallet connection)
  const fetchCounter = async () => {
    if (COUNTER_ID === '0x...') {
      setError('Counter not deployed yet.');
      return;
    }
    setIsLoading(true);
    setError('');
    try {
      const obj = await suiClient.getObject({
        id: COUNTER_ID,
        options: { showContent: true },
      });
      if (obj.data?.content?.dataType === 'moveObject') {
        const fields = obj.data.content.fields as { value: string };
        setCounterValue(parseInt(fields.value));
      }
    } catch (e: any) {
      console.error('Fetch error:', e);
      setError(`Failed to fetch counter`);
    } finally {
      setIsLoading(false);
    }
  };

  // Auto-fetch counter on mount
  useEffect(() => {
    fetchCounter();
  }, []);
  
  // Re-fetch when account changes
  useEffect(() => {
    if (account) {
      fetchCounter();
    }
  }, [account]);

  // Increment counter
  const increment = () => {
    const tx = new Transaction();
    tx.moveCall({
      target: `${PACKAGE_ID}::counter::increment`,
      arguments: [tx.object(COUNTER_ID)],
    });
    
    setStatus('Waiting for signature...');
    setError('');
    signAndExecute(
      { transaction: tx },
      {
        onSuccess: (result) => {
          setStatus(`Success! Tx: ${result.digest.slice(0, 12)}...`);
          setTimeout(fetchCounter, 1000);
        },
        onError: (e) => {
          setError(e.message);
          setStatus('');
        },
      }
    );
  };

  // Create new counter
  const createCounter = () => {
    const tx = new Transaction();
    tx.moveCall({
      target: `${PACKAGE_ID}::counter::create`,
    });
    
    setStatus('Creating counter...');
    signAndExecute(
      { transaction: tx },
      {
        onSuccess: (result) => {
          setStatus(`Created! Tx: ${result.digest.slice(0, 12)}...`);
          console.log('New counter created:', result);
        },
        onError: (e) => {
          setError(e.message);
          setStatus('');
        },
      }
    );
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.header}>
          <h1 style={styles.title}>🔢 Counter DApp</h1>
          <p style={styles.subtitle}>Sui Agent Wallet Demo</p>
        </div>

        <div style={styles.section}>
          <div style={styles.walletRow}>
            <ConnectButton 
              connectText="Connect Wallet"
              style={styles.connectBtn}
            />
          </div>
          {account && (
            <p style={styles.addressText}>
              {account.address.slice(0, 8)}...{account.address.slice(-6)}
            </p>
          )}
        </div>

        <div style={styles.counterSection}>
          <div style={styles.counterDisplay}>
            {isLoading ? (
              <span style={styles.counterValue}>...</span>
            ) : counterValue !== null ? (
              <span style={styles.counterValue}>{counterValue}</span>
            ) : (
              <span style={styles.counterPlaceholder}>—</span>
            )}
          </div>
          
          <div style={styles.buttonRow}>
            <button 
              onClick={fetchCounter} 
              style={styles.secondaryBtn}
              disabled={isLoading}
            >
              ↻ Refresh
            </button>
            <button 
              onClick={increment} 
              style={styles.primaryBtn}
              disabled={!account || isPending}
            >
              {isPending ? '...' : '+1'}
            </button>
          </div>
        </div>

        {(status || error) && (
          <div style={styles.statusSection}>
            {status && <p style={styles.statusText}>{status}</p>}
            {error && <p style={styles.errorText}>{error}</p>}
          </div>
        )}

        <div style={styles.footer}>
          <button 
            onClick={createCounter}
            style={styles.linkBtn}
            disabled={!account}
          >
            Create New Counter
          </button>
        </div>
      </div>

      <div style={styles.info}>
        <p><strong>Network:</strong> Testnet</p>
        <p><strong>Package:</strong> {PACKAGE_ID.slice(0, 10)}...</p>
      </div>
    </div>
  );
}

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '20px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  },
  card: {
    background: 'white',
    borderRadius: '24px',
    padding: '32px',
    width: '100%',
    maxWidth: '400px',
    boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
  },
  header: {
    textAlign: 'center',
    marginBottom: '24px',
  },
  title: {
    fontSize: '28px',
    fontWeight: '700',
    color: '#1a1a2e',
    margin: '0 0 8px 0',
  },
  subtitle: {
    fontSize: '14px',
    color: '#666',
    margin: 0,
  },
  section: {
    marginBottom: '24px',
  },
  walletRow: {
    display: 'flex',
    justifyContent: 'center',
  },
  connectBtn: {
    width: '100%',
  },
  addressText: {
    textAlign: 'center',
    fontSize: '13px',
    color: '#888',
    marginTop: '8px',
    fontFamily: 'monospace',
  },
  counterSection: {
    textAlign: 'center',
    marginBottom: '24px',
  },
  counterDisplay: {
    background: 'linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%)',
    borderRadius: '16px',
    padding: '32px',
    marginBottom: '16px',
  },
  counterValue: {
    fontSize: '64px',
    fontWeight: '700',
    color: '#1a1a2e',
  },
  counterPlaceholder: {
    fontSize: '48px',
    color: '#ccc',
  },
  buttonRow: {
    display: 'flex',
    gap: '12px',
    justifyContent: 'center',
  },
  primaryBtn: {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    borderRadius: '12px',
    padding: '14px 32px',
    fontSize: '18px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'transform 0.2s, box-shadow 0.2s',
  },
  secondaryBtn: {
    background: '#f0f0f0',
    color: '#333',
    border: 'none',
    borderRadius: '12px',
    padding: '14px 20px',
    fontSize: '16px',
    cursor: 'pointer',
  },
  statusSection: {
    textAlign: 'center',
    marginBottom: '16px',
  },
  statusText: {
    color: '#28a745',
    fontSize: '14px',
    margin: 0,
  },
  errorText: {
    color: '#dc3545',
    fontSize: '14px',
    margin: 0,
  },
  footer: {
    textAlign: 'center',
    borderTop: '1px solid #eee',
    paddingTop: '16px',
  },
  linkBtn: {
    background: 'none',
    border: 'none',
    color: '#667eea',
    fontSize: '14px',
    cursor: 'pointer',
    textDecoration: 'underline',
  },
  info: {
    marginTop: '24px',
    color: 'rgba(255,255,255,0.7)',
    fontSize: '12px',
    textAlign: 'center',
  },
};
