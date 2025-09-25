import React, { useState, useEffect, useCallback } from 'react';
import { useUser } from '../contexts/UserContext';
import { useEnhancedNotification } from './EnhancedNotificationSystem';
import './BlockchainIntegration.css';

const BlockchainIntegration = () => {
  const { user } = useUser();
  const { addNotification } = useEnhancedNotification();
  const [isConnected, setIsConnected] = useState(false);
  const [walletAddress, setWalletAddress] = useState('');
  const [balance, setBalance] = useState(0);
  const [transactions, setTransactions] = useState([]);
  const [smartContracts, setSmartContracts] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // 检查Web3支持
  useEffect(() => {
    if (typeof window.ethereum !== 'undefined') {
      setIsConnected(true);
      loadWalletInfo();
    } else {
      addNotification({
        type: 'warning',
        title: 'Web3未检测到',
        message: '请安装MetaMask或其他Web3钱包以使用区块链功能'
      });
    }
  }, [addNotification]);

  // 加载钱包信息
  const loadWalletInfo = useCallback(async () => {
    try {
      const accounts = await window.ethereum.request({ method: 'eth_accounts' });
      if (accounts.length > 0) {
        setWalletAddress(accounts[0]);
        await loadBalance(accounts[0]);
        await loadTransactions(accounts[0]);
      }
    } catch (error) {
      console.error('加载钱包信息失败:', error);
    }
  }, []);

  // 连接钱包
  const connectWallet = async () => {
    try {
      setIsLoading(true);
      const accounts = await window.ethereum.request({ 
        method: 'eth_requestAccounts' 
      });
      
      if (accounts.length > 0) {
        setWalletAddress(accounts[0]);
        setIsConnected(true);
        await loadBalance(accounts[0]);
        await loadTransactions(accounts[0]);
        
        addNotification({
          type: 'success',
          title: '钱包连接成功',
          message: `已连接到地址: ${accounts[0].slice(0, 6)}...${accounts[0].slice(-4)}`
        });
      }
    } catch (error) {
      console.error('连接钱包失败:', error);
      addNotification({
        type: 'error',
        title: '连接失败',
        message: '无法连接到钱包，请重试'
      });
    } finally {
      setIsLoading(false);
    }
  };

  // 断开钱包连接
  const disconnectWallet = () => {
    setWalletAddress('');
    setIsConnected(false);
    setBalance(0);
    setTransactions([]);
    addNotification({
      type: 'info',
      title: '钱包已断开',
      message: '已断开钱包连接'
    });
  };

  // 加载余额
  const loadBalance = async (address) => {
    try {
      const balance = await window.ethereum.request({
        method: 'eth_getBalance',
        params: [address, 'latest']
      });
      setBalance(parseInt(balance, 16) / Math.pow(10, 18));
    } catch (error) {
      console.error('加载余额失败:', error);
    }
  };

  // 加载交易记录
  const loadTransactions = async (address) => {
    try {
      // 这里应该调用实际的区块链API
      // 为了演示，我们使用模拟数据
      const mockTransactions = [
        {
          hash: '0x1234...5678',
          from: address,
          to: '0xabcd...efgh',
          value: '1.5',
          timestamp: Date.now() - 86400000,
          status: 'confirmed'
        },
        {
          hash: '0x2345...6789',
          from: '0xefgh...ijkl',
          to: address,
          value: '2.3',
          timestamp: Date.now() - 172800000,
          status: 'confirmed'
        }
      ];
      setTransactions(mockTransactions);
    } catch (error) {
      console.error('加载交易记录失败:', error);
    }
  };

  // 部署智能合约
  const deploySmartContract = async (contractData) => {
    try {
      setIsLoading(true);
      
      // 模拟智能合约部署
      const contractAddress = '0x' + Math.random().toString(16).substr(2, 40);
      
      const newContract = {
        address: contractAddress,
        name: contractData.name,
        type: contractData.type,
        deployedAt: Date.now(),
        status: 'deployed'
      };
      
      setSmartContracts(prev => [newContract, ...prev]);
      
      addNotification({
        type: 'success',
        title: '智能合约部署成功',
        message: `合约地址: ${contractAddress.slice(0, 6)}...${contractAddress.slice(-4)}`
      });
      
      return newContract;
    } catch (error) {
      console.error('部署智能合约失败:', error);
      addNotification({
        type: 'error',
        title: '部署失败',
        message: '智能合约部署失败，请重试'
      });
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  // 执行智能合约方法
  const executeContractMethod = async (contractAddress, method, params) => {
    try {
      setIsLoading(true);
      
      // 模拟智能合约方法执行
      const result = {
        transactionHash: '0x' + Math.random().toString(16).substr(2, 64),
        gasUsed: Math.floor(Math.random() * 100000),
        status: 'success'
      };
      
      addNotification({
        type: 'success',
        title: '合约方法执行成功',
        message: `交易哈希: ${result.transactionHash.slice(0, 10)}...`
      });
      
      return result;
    } catch (error) {
      console.error('执行合约方法失败:', error);
      addNotification({
        type: 'error',
        title: '执行失败',
        message: '合约方法执行失败，请重试'
      });
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  // 创建贷款智能合约
  const createLoanContract = async () => {
    const contractData = {
      name: 'AI Loan Contract',
      type: 'loan',
      description: '智能贷款合约，自动执行贷款条件'
    };
    
    return await deploySmartContract(contractData);
  };

  // 创建风险评估智能合约
  const createRiskAssessmentContract = async () => {
    const contractData = {
      name: 'Risk Assessment Contract',
      type: 'risk',
      description: '智能风险评估合约，基于链上数据评估风险'
    };
    
    return await deploySmartContract(contractData);
  };

  return (
    <div className="blockchain-integration">
      <div className="blockchain-header">
        <h2>区块链集成</h2>
        <p>连接Web3钱包，使用智能合约进行去中心化贷款服务</p>
      </div>

      {/* 钱包连接状态 */}
      <div className="wallet-section">
        <h3>钱包状态</h3>
        {!isConnected ? (
          <div className="wallet-disconnected">
            <div className="wallet-icon">🔗</div>
            <p>未连接钱包</p>
            <button 
              className="connect-btn"
              onClick={connectWallet}
              disabled={isLoading}
            >
              {isLoading ? '连接中...' : '连接钱包'}
            </button>
          </div>
        ) : (
          <div className="wallet-connected">
            <div className="wallet-info">
              <div className="wallet-address">
                <span className="label">地址:</span>
                <span className="value">{walletAddress}</span>
              </div>
              <div className="wallet-balance">
                <span className="label">余额:</span>
                <span className="value">{balance.toFixed(4)} ETH</span>
              </div>
            </div>
            <button 
              className="disconnect-btn"
              onClick={disconnectWallet}
            >
              断开连接
            </button>
          </div>
        )}
      </div>

      {/* 智能合约管理 */}
      {isConnected && (
        <div className="contracts-section">
          <h3>智能合约</h3>
          <div className="contract-actions">
            <button 
              className="contract-btn primary"
              onClick={createLoanContract}
              disabled={isLoading}
            >
              部署贷款合约
            </button>
            <button 
              className="contract-btn secondary"
              onClick={createRiskAssessmentContract}
              disabled={isLoading}
            >
              部署风险评估合约
            </button>
          </div>
          
          <div className="contracts-list">
            {smartContracts.map((contract, index) => (
              <ContractCard 
                key={index}
                contract={contract}
                onExecute={executeContractMethod}
              />
            ))}
          </div>
        </div>
      )}

      {/* 交易记录 */}
      {isConnected && (
        <div className="transactions-section">
          <h3>交易记录</h3>
          <div className="transactions-list">
            {transactions.map((tx, index) => (
              <TransactionCard key={index} transaction={tx} />
            ))}
          </div>
        </div>
      )}

      {/* 区块链功能说明 */}
      <div className="blockchain-features">
        <h3>区块链功能</h3>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">🔐</div>
            <h4>去中心化身份</h4>
            <p>基于区块链的数字身份验证，保护用户隐私</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📋</div>
            <h4>智能合约</h4>
            <p>自动执行贷款条件，减少人工干预</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🔍</div>
            <h4>透明审计</h4>
            <p>所有交易记录在区块链上公开透明</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h4>快速结算</h4>
            <p>基于区块链的快速资金结算</p>
          </div>
        </div>
      </div>
    </div>
  );
};

// 智能合约卡片组件
const ContractCard = ({ contract, onExecute }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const handleExecute = async () => {
    const method = 'executeLoan';
    const params = ['borrower', 'amount', 'interestRate'];
    await onExecute(contract.address, method, params);
  };

  return (
    <div className="contract-card">
      <div className="contract-header">
        <div className="contract-info">
          <h4>{contract.name}</h4>
          <p className="contract-address">
            {contract.address.slice(0, 6)}...{contract.address.slice(-4)}
          </p>
        </div>
        <button 
          className="expand-btn"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          {isExpanded ? '−' : '+'}
        </button>
      </div>
      
      {isExpanded && (
        <div className="contract-details">
          <div className="contract-meta">
            <span className="contract-type">{contract.type}</span>
            <span className="contract-status">{contract.status}</span>
          </div>
          <div className="contract-actions">
            <button 
              className="execute-btn"
              onClick={handleExecute}
            >
              执行合约
            </button>
            <button className="view-btn">
              查看详情
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

// 交易记录卡片组件
const TransactionCard = ({ transaction }) => {
  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleString('zh-CN');
  };

  return (
    <div className="transaction-card">
      <div className="transaction-header">
        <div className="transaction-hash">
          {transaction.hash.slice(0, 10)}...{transaction.hash.slice(-6)}
        </div>
        <div className={`transaction-status ${transaction.status}`}>
          {transaction.status}
        </div>
      </div>
      <div className="transaction-details">
        <div className="transaction-amount">
          {transaction.value} ETH
        </div>
        <div className="transaction-time">
          {formatTime(transaction.timestamp)}
        </div>
      </div>
    </div>
  );
};

export default BlockchainIntegration;