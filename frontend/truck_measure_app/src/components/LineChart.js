import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';
import { BASE_URL } from '../config/config';
import 'chart.js/auto';

const LineChart = () => {
    const [chartData, setChartData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`${BASE_URL}/api/v1/vehicle-details`);
                const data = response.data;

                const baseDate = new Date('2024-01-01');
                const groupedData = data.reduce((acc, detail) => {
                    const date = new Date(detail.created_at);
                    if (date < baseDate) return acc;
                    const month = date.toLocaleString('default', { month: 'short', year: 'numeric' });

                    if (!acc[month]) {
                        acc[month] = { count: 0, cumulative: 0 };
                    }
                    acc[month].count += 1;
                    return acc;
                }, {});

                let cumulativeCount = 0;
                const labels = [baseDate.toLocaleString('default', { month: 'short', year: 'numeric' }), ...Object.keys(groupedData).sort((a, b) => new Date(a) - new Date(b))];
                const counts = [0, ...labels.slice(1).map(label => groupedData[label].count)];
                const cumulativeCounts = [0, ...labels.slice(1).map(label => {
                    cumulativeCount += groupedData[label].count;
                    return cumulativeCount;
                })];

                setChartData({
                    labels,
                    datasets: [
                        {
                            label: 'Number of Trucks Added',
                            data: counts,
                            borderColor: 'rgba(75,192,192,1)',
                            backgroundColor: 'rgba(75,192,192,0.2)',
                        },
                        {
                            label: 'Cumulative Number of Trucks',
                            data: cumulativeCounts,
                            borderColor: 'rgba(153,102,255,1)',
                            backgroundColor: 'rgba(153,102,255,0.2)',
                        },
                    ],
                });
            } catch (error) {
                console.error('Error fetching vehicle details:', error);
            }
        };

        fetchData();
    }, []);

    if (!chartData) {
        return <div>Loading...</div>;
    }

    return (
        <div style={{ height: '400px' }}>
            <Line
                data={chartData}
                options={{
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Date (Month-Year)',
                                color: '#000', // Changed to black for better visibility
                            },
                            ticks: {
                                color: '#000', // Changed to black for better visibility
                                autoSkip: false,
                                maxRotation: 45,
                                minRotation: 45,
                            },
                            grid: {
                                color: 'rgba(0, 0, 0, 0.2)', // Changed to black for better visibility
                            },
                        },
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Number of Trucks',
                                color: '#000', // Changed to black for better visibility
                            },
                            ticks: {
                                precision: 0,
                                color: '#000', // Changed to black for better visibility
                            },
                            grid: {
                                color: 'rgba(0, 0, 0, 0.2)', // Changed to black for better visibility
                            },
                        },
                    },
                    plugins: {
                        legend: {
                            labels: {
                                color: '#000', // Changed to black for better visibility
                            },
                        },
                    },
                    elements: {
                        line: {
                            tension: 0.4,
                        },
                    },
                    responsive: true,
                    maintainAspectRatio: false,
                }}
            />
        </div>
    );
};

export default LineChart;
