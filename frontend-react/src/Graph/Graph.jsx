import styles from "./Graph.module.css"
import { Chart as ChartJS} from "chart.js/auto"
import { Line } from "react-chartjs-2"
import { useState, useEffect } from "react"

function Graph({metric}, vars) {

    return(
        <div className={styles.lineGraph}>
            <Line
                data = {{
                    labels: [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
                    datasets: [{
                        label: metric,
                        data: data[metric],
                        borderColor: 'red',
                        borderWidth: 1
                    }
                ]
                }}
                options={{
                    plugins: {
                        title: {
                            text: metric + " Metric",
                            font: { size: 14 },
                            display: true
                        },
                        legend: {
                            display: false
                        }
                    },
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            title: {
                                text: "Seconds Past",
                                font: { size: 14 },
                                display: true
                            },
                            reverse: true
                        },
                        y: {
                            title: {
                                text: "% Usage",
                                font: { size: 14 },
                                display: true
                            },
                            min: 0,
                            max: 100,
                            ticks: { stepSize: 20 }
                        }
                    }
                }}
            />
        </div>
    );
}

export default Graph;