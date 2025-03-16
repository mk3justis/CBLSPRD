import styles from "./Header.module.css"
import Myli from "../Myli/Myli.jsx"

function Header() {
    
    return(
        <header>
            <h1 className={styles.h1}>CBLSPRD</h1>
            <nav>
                <ul>
                    <Myli metric="CPU" vars={["cpu", "cpu0", "cpu1", "ctxt", "procs_running", "softirq"]} ></Myli>
                    <Myli metric="IO"></Myli>
                    <Myli metric="Filesystem"></Myli>
                    <Myli metric="Memory"></Myli>
                    <Myli metric="Scheduler"></Myli>
                    <Myli metric="Load"></Myli>
                </ul>
            </nav>
        </header>
    );
}

export default Header;