function isValidUUID(uuid: string): boolean {
  const uuidRegex =
    /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  return uuidRegex.test(uuid);
}

export function encodeUUID(uuid: string): string | null {
  try {
    // Validate the UUID format
    if (!isValidUUID(uuid)) {
      throw new Error("Invalid UUID format");
    }

    // Remove hyphens from the UUID
    const cleanUUID = uuid.replace(/-/g, "");

    // Convert the hex UUID to a Uint8Array (byte array)
    const byteArray = new Uint8Array(
      cleanUUID.match(/.{1,2}/g)!.map((byte) => parseInt(byte, 16)),
    );

    // Encode the byte array to Base64
    let base64String = btoa(String.fromCharCode(...byteArray));

    // Convert Base64 to URL-friendly Base64
    // Replace `+` with `-`, `/` with `_` and remove `=`
    base64String = base64String
      .replace(/\+/g, "-")
      .replace(/\//g, "_")
      .replace(/=+$/, "");

    return base64String;

  } catch (error) {
    return null;
  }
}

export function decodeUUID(base64: string): string | null {
  try {
    // Convert URL-friendly Base64 to standard Base64
    let standardBase64 = base64.replace(/-/g, "+").replace(/_/g, "/");

    // Add padding if necessary (Base64 length should be a multiple of 4)
    const paddingNeeded = 4 - (standardBase64.length % 4);
    if (paddingNeeded !== 4) {
      standardBase64 += "=".repeat(paddingNeeded);
    }

    // Decode the Base64 string into a byte array
    const binaryString = atob(standardBase64);
    const byteArray = new Uint8Array(
      [...binaryString].map((char) => char.charCodeAt(0)),
    );

    // Convert byte array back to hex string
    const hexString = Array.from(byteArray)
      .map((byte) => byte.toString(16).padStart(2, "0"))
      .join("");

    // Reformat the hex string into UUID format (8-4-4-4-12)
    const uuid = `${hexString.slice(0, 8)}-${hexString.slice(8, 12)}-${hexString.slice(12, 16)}-${hexString.slice(16, 20)}-${hexString.slice(20)}`;

    // Validate the UUID format
    if (!isValidUUID(uuid)) {
      throw new Error("Invalid UUID format");
    }

    return uuid;
  } catch (error) {
    return null;
  }
}
