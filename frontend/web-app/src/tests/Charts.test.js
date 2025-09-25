import React from 'react';
import { render, screen } from '@testing-library/react';
import { RiskDistribution, LoanTrend, RiskScoreDistribution } from '../components/Charts';

// 模拟数据
const mockRiskData = [
  { level: '低风险', count: 450, percentage: 36 },
  { level: '中风险', count: 350, percentage: 28 },
  { level: '高风险', count: 450, percentage: 36 }
];

const mockTrendData = [
  { month: '2025-03', total: 120, approved: 100, rejected: 20 },
  { month: '2025-04', total: 135, approved: 115, rejected: 20 }
];

const mockScoreData = [
  { range: '0-20', count: 50 },
  { range: '21-40', count: 100 },
  { range: '41-60', count: 200 },
  { range: '61-80', count: 150 },
  { range: '81-100', count: 100 }
];

describe('Charts Components', () => {
  test('renders RiskDistribution component', () => {
    render(<RiskDistribution data={mockRiskData} />);
    
    expect(screen.getByText('风险等级分布')).toBeInTheDocument();
  });

  test('renders LoanTrend component', () => {
    render(<LoanTrend data={mockTrendData} />);
    
    expect(screen.getByText('贷款申请趋势')).toBeInTheDocument();
  });

  test('renders RiskScoreDistribution component', () => {
    render(<RiskScoreDistribution data={mockScoreData} />);
    
    expect(screen.getByText('风险评分分布')).toBeInTheDocument();
  });

  test('handles empty data gracefully', () => {
    render(<RiskDistribution data={[]} />);
    
    expect(screen.getByText('风险等级分布')).toBeInTheDocument();
  });

  test('updates when data changes', () => {
    const { rerender } = render(<RiskDistribution data={mockRiskData} />);
    
    expect(screen.getByText('风险等级分布')).toBeInTheDocument();
    
    const newData = [
      { level: '低风险', count: 500, percentage: 40 },
      { level: '中风险', count: 400, percentage: 32 },
      { level: '高风险', count: 300, percentage: 28 }
    ];
    
    rerender(<RiskDistribution data={newData} />);
    
    expect(screen.getByText('风险等级分布')).toBeInTheDocument();
  });
});
