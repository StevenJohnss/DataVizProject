import React, { useState, useEffect, useMemo } from 'react';
import { motion } from 'framer-motion';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import api from '../api';

interface ProductStatistics {
  mean: number;
  median: number;
  mode: number[];
  outliers: number[];
  quartiles: {
    Q1: number;
    Q2: number;
    Q3: number;
  };
  total_quantity: number;
  total_sales: number;
}

interface GroupedStatisticalData {
  [productName: string]: ProductStatistics;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D', '#A4DE6C', '#D0ED57'];

const Dashboard: React.FC = () => {
  const [groupedStatisticalData, setGroupedStatisticalData] = useState<GroupedStatisticalData | null>(null);
  const [selectedProduct, setSelectedProduct] = useState<string | null>(null);

  useEffect(() => {
    const fetchStatisticalData = async () => {
      try {
        const response = await api.get<GroupedStatisticalData>('/sales/statistics');
        setGroupedStatisticalData(response.data);
      } catch (error) {
        console.error('Error fetching statistical data:', error);
      }
    };

    fetchStatisticalData();
  }, []);

  const productNames = groupedStatisticalData ? Object.keys(groupedStatisticalData) : [];

  const chartData = useMemo(() => {
    if (!groupedStatisticalData) return [];

    let data: ProductStatistics;

    if (selectedProduct) {
      data = groupedStatisticalData[selectedProduct];
    } else {
      // Aggregate data for all products
      data = Object.values(groupedStatisticalData).reduce(
        (acc, curr) => ({
          mean: acc.mean + curr.mean,
          median: acc.median + curr.median,
          mode: [...acc.mode, ...curr.mode],
          outliers: [...acc.outliers, ...curr.outliers],
          quartiles: {
            Q1: acc.quartiles.Q1 + curr.quartiles.Q1,
            Q2: acc.quartiles.Q2 + curr.quartiles.Q2,
            Q3: acc.quartiles.Q3 + curr.quartiles.Q3,
          },
          total_quantity: acc.total_quantity + curr.total_quantity,
          total_sales: acc.total_sales + curr.total_sales,
        }),
        {
          mean: 0,
          median: 0,
          mode: [],
          outliers: [],
          quartiles: { Q1: 0, Q2: 0, Q3: 0 },
          total_quantity: 0,
          total_sales: 0,
        }
      );

      // Calculate averages for mean, median, and quartiles
      const productCount = Object.keys(groupedStatisticalData).length;
      data.mean /= productCount;
      data.median /= productCount;
      data.quartiles.Q1 /= productCount;
      data.quartiles.Q2 /= productCount;
      data.quartiles.Q3 /= productCount;

      // For mode, we'll use the most frequent value across all products
      data.mode = [data.mode.reduce((a, b) => (
        data.mode.filter(v => v === a).length >= data.mode.filter(v => v === b).length ? a : b
      ), data.mode[0])];
    }

    if (!data) return [];

    return [
      { name: 'Mean', value: data.mean },
      { name: 'Median', value: data.median },
      { name: 'Mode', value: data.mode[0] },
      { name: 'Q1', value: data.quartiles.Q1 },
      { name: 'Q2', value: data.quartiles.Q2 },
      { name: 'Q3', value: data.quartiles.Q3 },
      { name: 'Total Quantity', value: data.total_quantity },
      { name: 'Total Sales', value: data.total_sales },
    ];
  }, [groupedStatisticalData, selectedProduct]);

  return (
    <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="px-4 py-6 sm:px-0"
      >
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Sales Statistics</h2>
            {groupedStatisticalData ? (
              <>
                <div className="mb-6">
                  <label htmlFor="product-select" className="block text-sm font-medium text-gray-700 mb-2">
                    Select Product
                  </label>
                  <div className="relative">
                    <select id="small" className="block w-full p-2 mb-6 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                      value={selectedProduct || ''}
                      onChange={(e) => setSelectedProduct(e.target.value || null)}
                    >
                      <option value="">All Products</option>
                      {productNames.map((name) => (
                        <option key={name} value={name}>
                          {name}
                        </option>
                      ))}
                    </select>

                  </div>
                </div>
                <ResponsiveContainer width="100%" height={400}>
                  <PieChart>
                    <Pie
                      data={chartData}
                      dataKey="value"
                      nameKey="name"
                      cx="50%"
                      cy="50%"
                      outerRadius={150}
                      fill="#8884d8"
                      label
                    >
                      {chartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </>
            ) : (
              <p className="text-gray-500 text-center py-8">Loading statistical data...</p>
            )}
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard;
