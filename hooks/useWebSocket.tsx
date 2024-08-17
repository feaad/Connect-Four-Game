import { useEffect, useRef, useState } from "react";
import SockJS from "sockjs-client";
import { Client, IMessage } from "@stomp/stompjs";

interface WebSocketOptions {
  url: string;
  token: string;
  onMessage: (data: any) => void;
}

interface WebSocketState {
  sendMessage: (destination: string, message: any) => void;
  isConnected: boolean;
}

const useWebSocket = ({
  url,
  token,
  onMessage,
}: WebSocketOptions): WebSocketState => {
  const [isConnected, setIsConnected] = useState(false);
  const stompClientRef = useRef<Client | null>(null);

  useEffect(() => {
    if (stompClientRef.current) {
      return;
    }

    console.log("Connecting to WebSocket...");
    const socket = new SockJS(url);

    const stompClient = new Client({
      webSocketFactory: () => socket,
      connectHeaders: {
        Authorization: `Bearer ${token}`,
      },
      reconnectDelay: 5000,
      onConnect: () => {
        console.log("Connected to WebSocket");
        setIsConnected(true);
      },
      onStompError: (frame) => {
        console.error("STOMP error:", frame);
        setIsConnected(false);
      },
      onWebSocketError: (event) => {
        console.error("WebSocket error:", event);
        console.error("Error details:", {
          message: event.message,
          code: event.code,
          reason: event.reason,
          wasClean: event.wasClean,
        });
        setIsConnected(false);
      },
      onWebSocketClose: () => {
        console.log("WebSocket closed");
        setIsConnected(false);
      },
    });

    stompClient.onUnhandledMessage = (message: IMessage) => {
      onMessage(JSON.parse(message.body));
    };

    stompClient.activate();
    stompClientRef.current = stompClient;

    return () => {
      if (stompClientRef.current) {
        stompClientRef.current.deactivate();
        stompClientRef.current = null;
      }
    };
  }, [url, token, onMessage]);

  const sendMessage = (destination: string, message: any) => {
    if (stompClientRef.current && isConnected) {
      stompClientRef.current.publish({
        destination,
        body: JSON.stringify(message),
      });
    } else {
      console.error("Cannot send message, not connected");
    }
  };

  return {
    sendMessage,
    isConnected,
  };
};

export default useWebSocket;
