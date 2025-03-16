import { useEffect, useState, useRef } from "react";

function WebSocket(){
    const [metric, setMetric] = useState("No metric selected");
    const [data, setData] = useState([]);
    const socketRef = useRef(null);

    useEffect(() => {
        // I don't know the external IP right now
        const socket = new WebSocket("ws:// /ws");
        socketRef.current = socket;

        socket.onmessage = (event) => {
            const data_json = JSON.parse(event.data);
            setData((prev) => [data_json, ...prev.slice(0,9)]);
        };

        socket.onclose = () => {
            console.log("WebSocket closed.");
        };

        return () => {
            if (socketRef.current) {
                socketRef.current.close();
            }
        };
    }, []);

    const sendMetric = () => {
        if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
            socketRef.current.send(metric);
            setMetric("");
        }
    }
    return(
        <div>
            <h2>WebSocket Messages</h2>
            <input
                type="text"
                value={metric}
                onChange={(e) => setMetric(e.target.value)}
            />
            <button onClick={sendMetric}>Send</button>

            <ul>
                {data.map((msg, index) => (
                    <li key={index}>{JSON.stringify(msg)}</li>
                ))}
            </ul>
        </div>
    );
};

export default WebSocket