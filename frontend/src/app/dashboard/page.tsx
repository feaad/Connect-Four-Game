"use client";

import { useEffect, useState } from "react";
import { logout } from "@/actions/logout";
import useWebSocket, { UseWebSocketProps } from "@/hooks/useWebSocket";
import { getPlayerId } from "@/actions/getPlayerId";

const Dashboard = () => {
  const [playerId, setPlayerId] = useState<string | null>(null);
  const [webSocketConfig, setWebSocketConfig] =
    useState<UseWebSocketProps | null>(null);

  useEffect(() => {
    const fetchPlayerId = async () => {
      const id = await getPlayerId();
      setPlayerId(id ?? null);
    };

    fetchPlayerId();
  }, []);

  useEffect(() => {
    if (playerId) {
      setWebSocketConfig({ path: "/player/" + playerId });
    }
  }, [playerId]);

  const { sendMessage, receivedMessage, connectionStatus } = useWebSocket(
    webSocketConfig ?? { path: "" },
  );

  const handleSendMessage = () => {
    sendMessage("Hello, WebSocket!");
  };


  return (
    <div>
      Dashboard
      <form action={logout}>
        <button
          type="submit"
          className="tooltip tooltip-right"
          data-tip="Sign Out"
        >
          Sign Out
        </button>
      </form>
      <div>
        <p>WebSocket Status: {connectionStatus}</p>
        <button onClick={handleSendMessage}>Send Message</button>
        {receivedMessage && <p>Received: {receivedMessage}</p>}
      </div>
    </div>
  );
};

export default Dashboard;
