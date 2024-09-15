// import { env } from "@/lib/env";
// import axios from "axios";
// import type { NextRequest } from "next/server";
// import { NextResponse } from "next/server";

// import { getCurrentUser } from "@/actions/getCurrentUser";


// export async function POST(req: NextRequest) {
//   try {

//     const { token } = await getCurrentUser();

//     const response = await axios.post(
//       `${env.API_URL}/match/request`,
//       {},
//       {
//         headers: {
//           Authorization: `Bearer ${token}`,
//         },
//       },
//     );

//     return NextResponse.json(response.data, { status: response.status });

//   } catch (error) {
//     return NextResponse.json(
//       { message: "Error requesting match" },
//       { status: 500 },
//     );
//   }

// }