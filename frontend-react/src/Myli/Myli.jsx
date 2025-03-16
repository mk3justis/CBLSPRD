import Graph from "../Graph/Graph.jsx"
import styles from "./Myli.module.css"
import { useState } from "react"

function Myli(props){
    const [metric, setMetric] = useState('');
    const clicked = (chosenMetric) => {
        setMetric(chosenMetric);
    };
    console.log(metric)
    return(
        <>
            <button className={styles.li} onClick={() => clicked(props.metric)}>{props.metric}</button>
            <Graph metric={props.metric}/>
        </>
    )
}

export default Myli