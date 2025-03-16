import type { Schema } from "../../data/resource"

// Use the prebuilt handler type from your Schema
type Handler = Schema["getVersion"]["functionHandler"]

export const handler: Handler = async (event) => {
  // You can add any logic here if needed
  return "1.0.0";
}