const wsProtocol = window.location.protocol === "https:" ? "wss://" : "ws://";
const wsUrl = wsProtocol + window.location.host + "/ws/online/";

const socket = new WebSocket(wsUrl);

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    if (data.online_count !== undefined) {
        document.getElementById("online-counter").innerText = data.online_count;
    }
};

socket.onclose = function(e) {
    console.log("Websocket closed");
};

socket.onerror = function(error) {
    console.error("Websocket error:", error);
};