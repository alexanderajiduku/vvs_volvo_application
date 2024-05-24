import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import axios from 'axios';
import { BASE_URL } from '../config/config';
import 'chart.js/auto';

const BarChart = () => {
    const [chartData, setChartData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`${BASE_URL}/api/v1/vehicle-details`);
                const data = response.data;

                // Group heights into ranges of 10 cm
                const heightDistribution = data.reduce((acc, detail) => {
                    const range = Math.floor(detail.height / 10) * 10;
                    if (!acc[range]) {
                        acc[range] = 0;
                    }
                    acc[range] += 1;
                    return acc;
                }, {});

                const labels = Object.keys(heightDistribution).map(range => `${range}-${+range + 9}`);
                const values = Object.values(heightDistribution);

                setChartData({
                    labels,
                    datasets: [
                        {
                            label: 'Height Distribution',
                            data: values,
                            backgroundColor: 'rgba(75,192,192,0.6)',
                            borderColor: 'rgba(75,192,192,1)',
                            borderWidth: 1,
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
        <div style={{ height: '400px', maxWidth: '800px', margin: '0 auto', padding: '20px', background: '#fff', borderRadius: '8px', boxShadow: '0 0 10px rgba(0,0,0,0.1)' }}>
            <Bar
                data={chartData}
                options={{
                    scales: {
                        x: {
                            display: false,  // Remove horizontal labels
                            grid: {
                                color: 'rgba(0, 0, 0, 0.2)', // Changed to black for better visibility
                            },
                        },
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Number of Vehicles',
                                color: '#000', // Changed to black for better visibility
                            },
                            ticks: {
                                precision: 0, // Ensures integer values are displayed
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
                    responsive: true,
                    maintainAspectRatio: false,
                    layout: {
                        padding: {
                            top: 20,
                            bottom: 20,
                        },
                    },
                }}
            />
        </div>
    );
};

export default BarChart;