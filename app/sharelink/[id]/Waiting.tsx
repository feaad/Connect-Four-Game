"use client";
import React, { use, useEffect, useState } from "react";
import useWebSocket, { UseWebSocketProps } from "@/hooks/useWebSocket";
import { useRouter } from "next/navigation";
import { faCopy, faCheck } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Link from "next/link";
import WaitScreen from "@/components/WaitScreen";

interface WaitingProps {
  invitationId: string;
  playerId: string;
  shareLink: string;
}

const Waiting = ({ invitationId, playerId, shareLink }: WaitingProps) => {
  const router = useRouter();

  const [isCopied, setIsCopied] = useState(false);

  const [webSocketConfig, setWebSocketConfig] =
    useState<UseWebSocketProps | null>(null);

  const { receivedMessage, connectionStatus } = useWebSocket({
    path: "/player/" + playerId,
  });

  const [initialized, setInitialized] = useState(false);

  useEffect(() => {
    if (connectionStatus != 1 && initialized) {
      router.push(shareLink);
    } else if (connectionStatus == 1 && !initialized) {
      setInitialized(true);
    }
  }, [connectionStatus]);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(shareLink);
      setIsCopied(true);

      // Reset the copied state after 2 seconds
      setTimeout(() => {
        setIsCopied(false);
      }, 2000);
    } catch (err) {
      console.error("Failed to copy!", err);
    }
  };

  useEffect(() => {
    if (receivedMessage) {
      const msg = JSON.parse(receivedMessage);

      if (!msg.message) {
        return;
      }

      const { message } = msg;

      if (
        message.message &&
        message.message.event_type &&
        message.message.event_type === "invitation update"
      ) {
        const { invitation_id, status, game_id } = message.message;

        if (invitationId === invitation_id && status === "Accepted") {
          router.push(`/game/${game_id}`);
        }
      }
    }
  }, [receivedMessage]);

  return (
    //   TODO: Make this visually appealing
    <div className="from indigo-500 from-bg-1 from-1% via-bg-2 via-1% to-bg-3 to-1% -m-11 h-screen w-screen bg-gradient-to-br">
      <div>
        {connectionStatus != 1 ? (
          <div>
            <div className="flex justify-center pt-60">
              <span className="loading loading-dots w-[10rem] bg-white" />
            </div>
            <div className="flex justify-center">
              <h1 className="font-sans text-xl text-white">Connecting</h1>
            </div>
          </div>
        ) : (
          <>
            <WaitScreen />
            <div className="join flex h-12 w-full flex-row items-center justify-center pt-20">
              <div className="join-item flex h-12 w-[40rem] rounded-lg bg-btn-colour pl-5 pr-5">
                <code className="m-auto block text-sm text-white">
                  {shareLink}
                </code>
              </div>
              <div
                className="tooltip"
                data-tip={isCopied ? "Copied!" : "Copy URL to Clipboard"}
              >
                <button
                  className="btn btn-square btn-outline join-item text-btn-colour"
                  onClick={handleCopy}
                >
                  {isCopied ? (
                    <FontAwesomeIcon icon={faCheck} size="xl" color="#FFFFFF" />
                  ) : (
                    <FontAwesomeIcon
                      icon={faCopy}
                      size="xl"
                      className="fa-beat"
                    />
                  )}
                </button>
              </div>
            </div>
            <div className="flex justify-center pt-10">
              <p className="font-sans text-sm text-white">
                Copy and share the link
              </p>
            </div>
          </>
        )}
        <div className="insert-x-0 absolute bottom-0 flex justify-center w-full pb-12">
          <div className="text-white">
            <Link href="/"> Resign from Game</Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Waiting;
