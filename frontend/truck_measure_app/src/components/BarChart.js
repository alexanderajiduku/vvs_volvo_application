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

                const heightDistribution = data.reduce((acc, detail) => {
                    if (!acc[detail.height]) {
                        acc[detail.height] = 0;
                    }
                    acc[detail.height] += 1;
                    return acc;
                }, {});

                const labels = Object.keys(heightDistribution);
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
        <Bar
            data={chartData}
            options={{
                scales: {
                    y: {
                        ticks: {
                            beginAtZero: true,
                            precision: 0, // Ensures integer values are displayed
                        },
                    },
                },
            }}
        />
    );
};

export default BarChart;
