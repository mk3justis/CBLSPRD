import styles from "./Graph.module.css"
import { Chart as ChartJS} from "chart.js/auto"
import { Line } from "react-chartjs-2"
import { useState, useEffect } from "react"

function Graph({metric}, vars) {

    const [data, setData] = useState([]);
    // const [io, setIo] = useState([]);
    // const [memory, setMemory] = useState([]);
    // const [filesystem, setFilesystem] = useState([]);
    // const [load, setLoad] = useState([]);

    useEffect(() => {
        const fetchData = () => {
            // server url
            let url='http://34.138.30.112:8080/'+metric.toLowerCase();
            fetch(url)
            .then(response => response.json())
            .then(fetchedData => {
                setData(fetchedData)
            })
        };

        fetchData();
        const intervalId = setInterval(fetchData, 1000);

        return () => clearInterval(intervalId);
    }, []);

    if (!data) {
        return <div>Loading...</div>;
    }
    console.log(data)
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