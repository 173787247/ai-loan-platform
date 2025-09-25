import React, { createContext, useContext, useState, useEffect } from 'react';

const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // 模拟用户数据
  const mockUsers = {
    admin: {
      id: '1',
      username: 'admin',
      email: 'admin@example.com',
      userType: 'admin',
      fullName: '系统管理员',
      avatar: '👨‍💼',
      permissions: ['all'],
      lastLogin: new Date().toISOString()
    },
    borrower1: {
      id: '2',
      username: 'borrower1',
      email: 'borrower1@example.com',
      userType: 'borrower',
      fullName: '张三',
      avatar: '👤',
      permissions: ['apply_loan', 'view_loans', 'view_my_analytics'],
      lastLogin: new Date().toISOString()
    },
    lender1: {
      id: '3',
      username: 'lender1',
      email: 'lender1@example.com',
      userType: 'lender',
      fullName: '李四',
      avatar: '👨‍💻',
      permissions: ['invest_loan', 'view_investments', 'view_market_analytics', 'view_investment_analytics'],
      lastLogin: new Date().toISOString()
    },
    test: {
      id: '4',
      username: 'test',
      email: 'test@example.com',
      userType: 'borrower',
      fullName: '测试用户',
      avatar: '🧪',
      permissions: ['apply_loan', 'view_loans', 'view_my_analytics'],
      lastLogin: new Date().toISOString()
    }
  };

  // 检查本地存储的用户信息
  useEffect(() => {
    const checkAuth = () => {
      try {
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
          const userData = JSON.parse(storedUser);
          setUser(userData);
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.error('Error parsing stored user data:', error);
        localStorage.removeItem('user');
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  // 登录函数
  const login = async (username, password) => {
    setIsLoading(true);
    
    try {
      // 模拟API调用延迟
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // 模拟登录验证
      const validPasswords = {
        'admin': 'admin123',
        'borrower1': 'borrower123',
        'lender1': 'lender123',
        'test': 'test123'
      };
      
      // 调试信息
      console.log('登录尝试:', { username, password });
      console.log('有效密码:', validPasswords[username]);
      console.log('用户存在:', !!mockUsers[username]);
      console.log('密码匹配:', password === validPasswords[username]);
      
      if (mockUsers[username] && password === validPasswords[username]) {
        const userData = { ...mockUsers[username] };
        userData.lastLogin = new Date().toISOString();
        
        setUser(userData);
        setIsAuthenticated(true);
        localStorage.setItem('user', JSON.stringify(userData));
        
        return { success: true, user: userData };
      } else {
        return { 
          success: false, 
          error: '用户名或密码错误' 
        };
      }
    } catch (error) {
      return { 
        success: false, 
        error: '登录失败，请重试' 
      };
    } finally {
      setIsLoading(false);
    }
  };

  // 注册函数
  const register = async (userData) => {
    setIsLoading(true);
    
    try {
      // 模拟API调用延迟
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // 模拟注册验证
      if (mockUsers[userData.username]) {
        return { 
          success: false, 
          error: '用户名已存在' 
        };
      }
      
      const newUser = {
        id: Date.now(),
        username: userData.username,
        email: userData.email,
        userType: userData.userType,
        fullName: userData.fullName || userData.username,
        avatar: '👤',
        permissions: userData.userType === 'admin' ? ['all'] : 
                    userData.userType === 'borrower' ? ['apply_loan', 'view_loans'] :
                    ['invest_loan', 'view_investments'],
        lastLogin: new Date().toISOString()
      };
      
      setUser(newUser);
      setIsAuthenticated(true);
      localStorage.setItem('user', JSON.stringify(newUser));
      
      return { success: true, user: newUser };
    } catch (error) {
      return { 
        success: false, 
        error: '注册失败，请重试' 
      };
    } finally {
      setIsLoading(false);
    }
  };

  // 登出函数
  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem('user');
  };

  // 更新用户信息
  const updateUser = (updates) => {
    const updatedUser = { ...user, ...updates };
    setUser(updatedUser);
    localStorage.setItem('user', JSON.stringify(updatedUser));
  };

  // 检查权限
  const hasPermission = (permission) => {
    if (!user) return false;
    if (user.permissions.includes('all')) return true;
    return user.permissions.includes(permission);
  };

  // 检查用户类型
  const isUserType = (type) => {
    return user && user.userType === type;
  };

  // 检查是否为管理员
  const isAdmin = () => {
    return isUserType('admin');
  };

  // 检查是否为借款方
  const isBorrower = () => {
    return isUserType('borrower');
  };

  // 检查是否为放贷方
  const isLender = () => {
    return isUserType('lender');
  };

  const value = {
    user,
    isLoading,
    isAuthenticated: () => isAuthenticated,
    login,
    register,
    logout,
    updateUser,
    hasPermission,
    isUserType,
    isAdmin,
    isBorrower,
    isLender
  };

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};

export default UserContext;