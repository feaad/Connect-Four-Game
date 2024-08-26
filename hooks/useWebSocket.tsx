import { getCurrentUser } from "@/actions/getCurrentUser";
import { useCallback, useEffect, useRef, useState } from "react";

import { getWSUrl } from "@/actions/getWSUrl";

export interface UseWebSocketProps {
  path: string;
}

interface UseWebSocketReturn {
  sendMessage: (message: string) => void;
  receivedMessage: string | null;
  connectionStatus: WebSocket["readyState"];
}

let existingSocket: WebSocket | null = null;

const useWebSocket = ({ path }: UseWebSocketProps): UseWebSocketReturn => {
  const [receivedMessage, setReceivedMessage] = useState<string | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<
    WebSocket["readyState"]
  >(WebSocket.CONNECTING);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const establishConnection = async () => {
      if (existingSocket) {
        // Use the existing WebSocket connection
        socketRef.current = existingSocket;
        setConnectionStatus(existingSocket.readyState);
        console.log("Using existing WebSocket connection");
      } else {
        if (!path) {
          console.error("WebSocket path is required");
          return;
        }
        const url = (await getWSUrl()) + path;
        // const url = "ws://localhost:9080/ws" + path;

        const wsUrl = new URL(url);
        wsUrl.protocol = wsUrl.protocol === "https:" ? "wss:" : "ws:";

        // Await the token before creating the WebSocket
        const {token} = await getCurrentUser();
        if (token) {
          wsUrl.searchParams.append("token", token);
        }

        const socket = new WebSocket(wsUrl.toString());

        socket.onopen = () => {
          existingSocket = socket; // Save the connection globally
          socketRef.current = socket;
          setConnectionStatus(socket.readyState);
          console.log("WebSocket connection established");
        };

        socket.onmessage = (event) => {
          setReceivedMessage(event.data.toString());
        };

        socket.onclose = () => {
          setConnectionStatus(socket.readyState);
          console.log("WebSocket connection closed");
          existingSocket = null; // Reset the global reference on close
        };

        socket.onerror = (error) => {
          console.error("WebSocket error", error);
        };
      }
    };

    establishConnection();

    // Cleanup function to avoid memory leaks
    return () => {
      if (
        socketRef.current &&
        socketRef.current.readyState === WebSocket.CLOSED
      ) {
        existingSocket = null;
      }
    };
  }, [path]);

  const sendMessage = useCallback((message: string) => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(message);
    } else {
      console.warn("WebSocket is not open. Cannot send message.");
    }
  }, []);

  return { sendMessage, receivedMessage, connectionStatus };
};

export default useWebSocket;
