import { OpenFeature, Client } from "@openfeature/js-sdk";
import { FlagdProvider } from "@openfeature/flagd-provider";

const FLAGD_HOST = process.env.FLAGD_HOST ?? "localhost";
const FLAGD_PORT = Number(process.env.FLAGD_PORT ?? "8013");

let clientPromise: Promise<Client> | null = null;

async function initialiseClient(): Promise<Client> {
  const provider = new FlagdProvider({
    host: FLAGD_HOST,
    port: FLAGD_PORT,
  });

  OpenFeature.setProvider(provider);
  return OpenFeature.getClient("agentic-canon");
}

export async function getClient(): Promise<Client> {
  if (!clientPromise) {
    clientPromise = initialiseClient();
  }
  return clientPromise;
}

export async function getBoolean(
  flagKey: string,
  defaultValue = false,
): Promise<boolean> {
  try {
    const client = await getClient();
    return client.getBooleanValue(flagKey, defaultValue);
  } catch (error) {
    console.warn(`Flag evaluation failed for ${flagKey}:`, error);
    return defaultValue;
  }
}
