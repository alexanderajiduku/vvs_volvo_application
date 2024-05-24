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

                const groupedData = data.reduce((acc, detail) => {
                    const date = new Date(detail.created_at);
                    const month = date.toLocaleString('default', { month: 'short', year: 'numeric' });

                    if (!acc[month]) {
                        acc[month] = 0;
                    }
                    acc[month] += 1;
                    return acc;
                }, {});

                const labels = Object.keys(groupedData).sort((a, b) => new Date(a) - new Date(b));
                const values = labels.map(label => groupedData[label]);

                setChartData({
                    labels,
                    datasets: [
                        {
                            label: 'Number of Trucks',
                            data: values,
                            borderColor: 'rgba(75,192,192,1)',
                            backgroundColor: 'rgba(75,192,192,0.2)',
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
        <Line
            data={chartData}
            options={{
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Date (Month-Year)',
                            color: '#fff',
                        },
                        ticks: {
                            color: '#fff',
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.2)',
                        },
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Trucks',
                            color: '#fff',
                        },
                        ticks: {
                            precision: 0, // Ensures integer values are displayed
                            color: '#fff',
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.2)',
                        },
                    },
                },
                plugins: {
                    legend: {
                        labels: {
                            color: '#fff',
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
    );
};

export default LineChart;
