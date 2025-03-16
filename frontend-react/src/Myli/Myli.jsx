import Graph from "../Graph/Graph.jsx"
import styles from "./Myli.module.css"
import { useEffect, useState } from "react"

function Myli(props){
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchData = () => {
            // server url
            let url='http://34.138.30.112:8080/'+props.metric.toLowerCase();
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
        <>
            <div className={styles.li}>{props.metric}</div>
            <Graph metric={props.metric}/>
        </>
    )
}

export default Myli