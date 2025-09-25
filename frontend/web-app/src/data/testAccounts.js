// 测试账号数据
export const testAccounts = [
  {
    id: 1,
    username: 'admin',
    email: 'admin@example.com',
    password: 'admin123',
    userType: 'admin',
    displayName: '系统管理员'
  },
  {
    id: 2,
    username: 'borrower1',
    email: 'borrower1@example.com',
    password: 'borrower123',
    userType: 'borrower',
    displayName: '借款方A'
  },
  {
    id: 3,
    username: 'lender1',
    email: 'lender1@example.com',
    password: 'lender123',
    userType: 'lender',
    displayName: '放贷方A'
  },
  {
    id: 4,
    username: 'test',
    email: 'test@example.com',
    password: 'test123',
    userType: 'borrower',
    displayName: '测试用户'
  }
];

// 快速登录账号信息
export const quickLoginAccounts = [
  {
    type: 'admin',
    username: 'admin',
    password: 'admin123',
    description: '管理员账号 - 可访问所有功能'
  },
  {
    type: 'borrower',
    username: 'borrower1',
    password: 'borrower123',
    description: '借款方账号 - 可申请贷款'
  },
  {
    type: 'lender',
    username: 'lender1',
    password: 'lender123',
    description: '放贷方账号 - 可投资放贷'
  },
  {
    type: 'test',
    username: 'test',
    password: 'test123',
    description: '测试账号 - 通用测试'
  }
];
