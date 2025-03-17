// import styles from "./Graph.module.css"
// import { Chart } from "chart.js/auto"
// import { Line } from "react-chartjs-2"
// import { useState, useEffect, useRef, useMemo } from "react"

// function Graph({ metric, data }) {
//     const key = metric.toLowerCase() + "_stats"
//     const colors=['red', 'blue', 'green', 'yellow']

//     const dataDict = useMemo(() => {
//         let tempDataDict = {}
//         let count = 0
//         for (let stat in data[key]) {
//             let yValues = data[key][stat];
//             if (yValues.length < 10) {
//                 while (yValues.length < 10) {
//                     const padding = Array(10 - yValues.length).fill(0);
//                     yValues = padding.concat(yValues);  // You could also use `null` or another default value
//                 }
//             }
//             tempDataDict[stat]={label: stat, data: yValues, color: colors[count]};
//             count++;
//         }
//         return tempDataDict;
//     }, [data, key]);

//     const chartRef = useRef(null);
//     const chartInstance = useRef(null);

//     useEffect(() => {
//         if (chartInstance.current) {
//             chartInstance.current.destroy();
//         }

//         const ctx = chartRef.current.getContext("2d");

//         const datasets = Object.keys(dataDict).map(key => ({
//             label: dataDict[key].label,
//             data: dataDict[key].data,
//             borderColor: dataDict[key].color,
//             fill: false
//         }));

//         chartInstance.current = new Chart(ctx, {
//             type: "line",
//             data: {
//                 labels: [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
//                 datasets: datasets
//             },
//             options: {
//                 animation: false,
//                 responsive: true,
//                 plugins: {
//                     legend: { position: "top" }
//                 }
//             }

//         });

//     }, [dataDict]);

//     return(
//         <div>
//             <canvas ref={chartRef}></canvas>
//         </div>
//     );
// };

// export default Graph;

// ========================================= //
// RENDERING BUG: FOLLOW THESE STEPS FOR NOW //
// 1. COMMENT CODE BELOW                     //
// 2. UNCOMMENT CODE ABOVE AND SAVE          //
// 3. COMMENT CODE ABOVE                     //
// 4. UNCOMMENT CODE BELOW AND SAVE          //
// ========================================= //

import { useEffect, useRef, useState } from "react";
import { Chart } from "chart.js/auto";

// Uses props to pull in data from Myli components
function Graph({ metric, data }) {
    if (!data) {
        return <div>Loading...</div>;
    }

    console.log(data)
    // Uses hooks to create a chart reference and instance for use later
    const chartRef = useRef(null);
    const chartInstance = useRef(null);

    // Calculate key names to use dictionary data from prop
    const key = metric.toLowerCase() + "_stats";
    // Line colors
    const colors = ["red", "blue", "green", "yellow"];
    // x axis labels (compensates for rate of which graphs are updated)
    const x_labels = Array.from({ length: 20 }, (_, i) => {
        const label = 20-i;
        return label % 2 === 0 ? `${label/2}s` : " ";
    });
    // Uses hook to create chart without rerendering it in a loop
    const [chartData, setChartData] = useState({
        labels: x_labels,
        // Dynamically add datasets for the amount of fields in the data prop
        // This handles the differing number of lines in each graph
        datasets: Object.keys(data[key]).map((stat, index) => ({
            label: `${stat}`,
            // Makes the lines show realtime by storing the old values
            data: [...data[key][stat]].slice(-20),
            borderColor: colors[index % colors.length],
            fill: false
        }))
    });

    // If there is a chart instance already we need to destroy it, apparently
    useEffect(() => {
        if (chartInstance.current) {
            chartInstance.current.destroy();
        }

        // Creates the line graph using Chart.js with the chartData hook
        const ctx = chartRef.current.getContext("2d");
        chartInstance.current = new Chart(ctx, {
            type: "line",
            data: chartData,
            options: {
                responsive: true,
                animation: false,
                scales: {
                    x: { title: { display: true, text: "Time (Last 10s)" } },
                    y: { title: { display: true, text: metric }, ticks: { beginAtZero: false } }
                },
                plugins: {
                    legend: { position: "top" }
                }
            }
        });

    }, [chartData]);

    // This handles the lines updating in realtime
    // Have to update the chart data to add the new point
    useEffect(() => {
        const interval = setInterval(() => {
            if (!data[key]) return;
    
            setChartData(prevData => ({
                labels: x_labels,
                datasets: prevData.datasets.map(dataset => {
                    const statData = data[key][dataset.label];
    
                    if (statData && statData.length > 0) {
                        const newData = [...dataset.data.slice(1), statData[statData.length - 1]];
                        return {
                            ...dataset,
                            data: newData
                        };
                    }
    
                    return dataset;
                })
            }));
        // Update with a new point every half-second
        }, 500);
    
        return () => clearInterval(interval);
    }, [data[key]]);

    // Return the chart reference from the hook
    return (
        <div>
            <canvas ref={chartRef}></canvas>
        </div>
    );
}

export default Graph;
