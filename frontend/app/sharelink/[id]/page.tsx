import React from "react";
import { getInvitation } from "@/actions/getInvitation";
import { acceptInvitation } from "@/actions/acceptInvitation";
import { decodeUUID } from "@/lib/transformer";
import { redirect } from "next/navigation";
import { getCurrentUser } from "@/actions/getCurrentUser";

import { env } from "@/lib/env";

import Waiting from "./Waiting";

/**
 * The function `ShareLink` handles different scenarios based on the invitation details and provides
 * appropriate visual feedback for each case.
 * @param {ShareLinkProps}  - The code snippet you provided is a function called `ShareLink` that takes
 * a `ShareLinkProps` object as a parameter. The `ShareLinkProps` interface defines a single property
 * `params` which has an `id` property of type string.
 * @returns The ShareLink function returns different JSX elements based on the conditions met during
 * its execution. These JSX elements include:
 * - `<div>Invalid invitation ID</div>` if the invitation ID cannot be decoded
 * - `<div>Invitation not found</div>` if the invite is not found
 * - `<div>Invalid Player</div>` if the player ID is invalid
 * - `<Waiting ... />`
 */
interface ShareLinkProps {
  params: {
    id: string;
  };
}

/**
 * The ShareLink function in TypeScript React handles different scenarios related to invitations and
 * redirects users accordingly.
 * @param {ShareLinkProps}  - The code you provided is an asynchronous function called `ShareLink` that
 * takes a `ShareLinkProps` object as a parameter. The `ShareLinkProps` object has a `params` property
 * which contains an `id`. The function decodes the `id` using the `decodeUUID` function
 * @returns The function `ShareLink` returns different JSX elements based on the conditions met during
 * its execution. These elements include:
 * 1. `<div>Invalid invitation ID</div>` if the `invitationId` is invalid.
 * 2. `<div>Invitation not found</div>` if the invite is not found.
 * 3. `<div>Invalid Player</div>` if the player ID is invalid.
 * 4. `<Waiting ... />` if the sender is the same as the username and the receiver is not set.
 * 5. `<div>No Game ID</div>` if the game ID is not found.
 * 6. `<div>Invalid Invitation</div>` if the invitation is invalid.
 * 7. `<div>Invalid Invitation</div>` if the invitation is invalid.
 * 
 */
async function ShareLink({ params: { id } }: ShareLinkProps) {
  const invitationId = decodeUUID(id);

  if (!invitationId) {
    // TODO: Make this visually appealing

    return <div>Invalid invitation ID</div>;
  }

  const invite = await getInvitation(invitationId);

  if (!invite) {
    // TODO: Make this visually appealing
    return <div>Invitation not found</div>;
  }

  if (
    invite.gameId &&
    [invite.sender, invite.receiver].includes(invite.username)
  ) {
    redirect(`/game/${invite.gameId}`);
  }

  if (invite.sender === invite.username && !invite.receiver) {
    const { playerId } = await getCurrentUser();

    if (!playerId) {
      return <div>Invalid Player</div>;
    }

    return (
      <Waiting
        invitationId={invitationId}
        playerId={playerId}
        shareLink={`${env.NEXTAUTH_URL}/sharelink/${id}`}
      />
    );
  } else if (invite.sender !== invite.username && !invite.receiver) {
    const gameId = await acceptInvitation(invitationId);

    if (gameId) {
      redirect(`/game/${gameId}`);
    } else {
      // TODO: Make this viusally appealing
      return <div>No Game ID</div>;
    }
  } else {
    // TODO: Make this viusally appealing
    return <div>Invalid Invitation</div>;
  }
}

export default ShareLink;
