import { useState, useEffect } from 'react';
import { getTranslation } from '../translations';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement,
} from 'chart.js';
import { Line, Pie, Bar } from 'react-chartjs-2';
import WeatherWidget from './WeatherWidget';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement
);

const Dashboard = ({ language = 'en' }) => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [timeRange, setTimeRange] = useState(30);

  useEffect(() => {
    fetchDashboardStats();
  }, [timeRange]);

  const fetchDashboardStats = async () => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:8000/api/dashboard/stats/?days=${timeRange}`, {
        credentials: 'include'
      });
      const data = await response.json();
      setStats(data);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  const exportData = () => {
    if (!stats) return;

    // Create CSV content
    let csvContent = 'Category,Value\n';
    csvContent += `Total Predictions,${stats.total_predictions}\n`;
    csvContent += `Unique Users,${stats.unique_users}\n`;
    csvContent += `Treatment Success Rate,${stats.treatment_effectiveness?.average || 0}\n\n`;

    // Disease distribution
    csvContent += 'Disease Distribution\n';
    csvContent += 'Disease,Count\n';
    stats.disease_distribution?.forEach(item => {
      csvContent += `${item.disease__name},${item.count}\n`;
    });

    // Regional distribution
    csvContent += '\nRegional Distribution\n';
    csvContent += 'Region,Count\n';
    stats.regional_distribution?.forEach(item => {
      csvContent += `${item.location || 'Unknown'},${item.count}\n`;
    });

    // Create and download file
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `crop_disease_analytics_${timeRange}_days.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-md mx-auto bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">{error}</p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-3xl font-bold text-gray-900">{getTranslation('agriculturalDashboard', language)}</h1>
          <div className="flex items-center space-x-4">
            <button
              onClick={exportData}
              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors"
            >
              {getTranslation('exportCSV', language)}
            </button>
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(parseInt(e.target.value))}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            >
              <option value={7}>{getTranslation('last7Days', language) || 'Last 7 days'}</option>
              <option value={30}>{getTranslation('last30Days', language) || 'Last 30 days'}</option>
              <option value={90}>{getTranslation('last90Days', language) || 'Last 90 days'}</option>
            </select>
          </div>
        </div>
        <p className="text-gray-600">
          {getTranslation('comprehensiveAnalytics', language)}
        </p>
        {stats?.date_range && (
          <p className="text-sm text-gray-500 mt-2">
            Data from {stats.date_range.start} to {stats.date_range.end}
          </p>
        )}
      </div>

      {/* Weather Widget */}
      <div className="mb-6">
        <WeatherWidget language={language} />
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-xl shadow-md p-6">
          <div className="flex items-center">
            <div className="p-3 bg-blue-100 rounded-full">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">{getTranslation('totalPredictions', language)}</p>
              <p className="text-2xl font-bold text-gray-900">{stats?.total_predictions || 0}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <div className="flex items-center">
            <div className="p-3 bg-green-100 rounded-full">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">{getTranslation('activeUsers', language)}</p>
              <p className="text-2xl font-bold text-gray-900">{stats?.unique_users || 0}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <div className="flex items-center">
            <div className="p-3 bg-yellow-100 rounded-full">
              <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">{getTranslation('diseasesDetected', language)}</p>
              <p className="text-2xl font-bold text-gray-900">{stats?.disease_distribution?.length || 0}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <div className="flex items-center">
            <div className="p-3 bg-purple-100 rounded-full">
              <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">{getTranslation('treatmentSuccess', language)}</p>
              <p className="text-2xl font-bold text-gray-900">
                {stats?.treatment_effectiveness?.average ? `${stats.treatment_effectiveness.average.toFixed(1)}/5` : 'N/A'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Daily Trend Chart */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">{getTranslation('dailyPredictionTrend', language) || 'Daily Prediction Trend'}</h3>
          <div className="h-64">
            {stats?.daily_trend && stats.daily_trend.length > 0 ? (
              <Line
                data={{
                  labels: stats.daily_trend.map(item => new Date(item.date).toLocaleDateString()),
                  datasets: [{
                    label: 'Predictions',
                    data: stats.daily_trend.map(item => item.count),
                    borderColor: 'rgb(34, 197, 94)',
                    backgroundColor: 'rgba(34, 197, 94, 0.1)',
                    tension: 0.4,
                    fill: true,
                  }]
                }}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: { display: false },
                  },
                  scales: {
                    y: {
                      beginAtZero: true,
                      ticks: { precision: 0 }
                    }
                  }
                }}
              />
            ) : (
              <div className="flex items-center justify-center h-full text-gray-500">
                No data available for the selected period
              </div>
            )}
          </div>
        </div>

        {/* Disease Distribution Pie Chart */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">{getTranslation('diseaseDistribution', language)}</h3>
          <div className="h-64">
            {stats?.disease_distribution && stats.disease_distribution.length > 0 ? (
              <Pie
                data={{
                  labels: stats.disease_distribution.slice(0, 8).map(item => item.disease__name),
                  datasets: [{
                    data: stats.disease_distribution.slice(0, 8).map(item => item.count),
                    backgroundColor: [
                      '#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6',
                      '#8b5cf6', '#ec4899', '#6b7280'
                    ],
                    borderWidth: 2,
                    borderColor: '#ffffff',
                  }]
                }}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      position: 'bottom',
                      labels: { boxWidth: 12, font: { size: 11 } }
                    }
                  }
                }}
              />
            ) : (
              <div className="flex items-center justify-center h-full text-gray-500">
                No disease data available
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Additional Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Regional Distribution Bar Chart */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">{getTranslation('regionalDistribution', language)}</h3>
          <div className="h-64">
            {stats?.regional_distribution && stats.regional_distribution.length > 0 ? (
              <Bar
                data={{
                  labels: stats.regional_distribution.slice(0, 8).map(item => item.location || 'Unknown'),
                  datasets: [{
                    label: 'Predictions',
                    data: stats.regional_distribution.slice(0, 8).map(item => item.count),
                    backgroundColor: 'rgba(59, 130, 246, 0.8)',
                    borderColor: 'rgb(59, 130, 246)',
                    borderWidth: 1,
                  }]
                }}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: { display: false },
                  },
                  scales: {
                    y: {
                      beginAtZero: true,
                      ticks: { precision: 0 }
                    }
                  }
                }}
              />
            ) : (
              <div className="flex items-center justify-center h-full text-gray-500">
                No regional data available
              </div>
            )}
          </div>
        </div>

        {/* Treatment Effectiveness */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">{getTranslation('treatmentEffectiveness', language) || 'Treatment Effectiveness'}</h3>
          <div className="space-y-4">
            <div className="text-center">
              <div className="text-4xl font-bold text-green-600 mb-2">
                {stats?.treatment_effectiveness?.average ? `${stats.treatment_effectiveness.average.toFixed(1)}/5` : 'N/A'}
              </div>
              <p className="text-gray-600">Average Rating</p>
            </div>
            <div className="text-center">
              <div className="text-2xl font-semibold text-blue-600 mb-1">
                {stats?.treatment_effectiveness?.total_rated || 0}
              </div>
              <p className="text-gray-600">Treatments Rated</p>
            </div>
            {stats?.treatment_effectiveness?.total_rated > 0 && (
              <div className="mt-4">
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className="bg-green-600 h-3 rounded-full"
                    style={{ width: `${(stats.treatment_effectiveness.average / 5) * 100}%` }}
                  ></div>
                </div>
                <p className="text-xs text-gray-500 mt-1 text-center">Effectiveness Level</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Recent Predictions */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{getTranslation('recentPredictions', language)}</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Disease
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Confidence
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  User
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Location
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {stats?.recent_predictions?.map((prediction) => (
                <tr key={prediction.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {prediction.disease}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {(prediction.confidence * 100).toFixed(1)}%
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {prediction.user}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {prediction.location || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {new Date(prediction.created_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;