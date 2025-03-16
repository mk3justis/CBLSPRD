import styles from "./Header.module.css"
import Myli from "../Myli/Myli.jsx"

function Header() {
    
    return(
        <header>
            <h1 className={styles.h1}>CBLSPRD</h1>
            <nav>
                <ul>
                    <Myli metric="CPU" vars={["cpu", "cpu0", "cpu1", "ctxt", "procs_running", "softirq"]} ></Myli>
                    <Myli metric="IO" vars={["reads", "writes", "ios"]}></Myli>
                    <Myli metric="Memory" vars={["MemFree"]}></Myli>
                    <Myli metric="Scheduler" vars={["cpu_runtime", "cpu_waittime"]}></Myli>
                    <Myli metric="Load" vars={["one", "five", "fifteen"]}></Myli>
                </ul>
            </nav>
        </header>
    );
}

export default Header;