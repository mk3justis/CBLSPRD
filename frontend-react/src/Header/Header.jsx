import styles from "./Header.module.css"
import Myli from "../Myli/Myli.jsx"

function Header() {
    
    return(
        <header>
            <h1 className={styles.h1}>CBLSPRD</h1>
            <nav>
                <ul>
                    <Myli metric="CPU" vars={["cpu", "cpu0", "cpu1", "ctxt", "procs_running", "softirq"]} ></Myli>
                    <Myli metric="IO" vars={["reads0", "writes4", "ios8"]}></Myli>
                    <Myli metric="Memory" vars={["MemFree"]}></Myli>
                    <Myli metric="Scheduler" vars={["running6", "waiting7"]}></Myli>
                    <Myli metric="Load" vars={["one", "five", "fifteen"]}></Myli>
                </ul>
            </nav>
        </header>
    );
}

export default Header;