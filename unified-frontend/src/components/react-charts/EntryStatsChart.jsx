import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const EntryStatsChart = ({ data }) => {
  // 模拟数据 - 在实际应用中，这些数据应该从API获取
  const chartData = data || [
    { date: '2024-01', 词条数: 12, 浏览量: 156, 点赞数: 8 },
    { date: '2024-02', 词条数: 18, 浏览量: 234, 点赞数: 15 },
    { date: '2024-03', 词条数: 25, 浏览量: 345, 点赞数: 22 },
    { date: '2024-04', 词条数: 32, 浏览量: 421, 点赞数: 28 },
    { date: '2024-05', 词条数: 40, 浏览量: 512, 点赞数: 35 },
    { date: '2024-06', 词条数: 48, 浏览量: 623, 点赞数: 42 },
  ];

  return (
    <div style={{ width: '100%', height: 400 }}>
      <h3 style={{ textAlign: 'center', marginBottom: '20px', color: '#1890ff' }}>
        词条统计趋势图
      </h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={chartData}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip 
            formatter={(value, name) => [value, {
              '词条数': '词条数量',
              '浏览量': '浏览次数',
              '点赞数': '点赞数量'
            }[name]]}
          />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="词条数" 
            stroke="#1890ff" 
            activeDot={{ r: 8 }} 
            strokeWidth={2}
          />
          <Line 
            type="monotone" 
            dataKey="浏览量" 
            stroke="#52c41a" 
            strokeWidth={2}
          />
          <Line 
            type="monotone" 
            dataKey="点赞数" 
            stroke="#faad14" 
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default EntryStatsChart;