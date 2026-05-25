import { ExpoConfig, ConfigContext } from "expo/config";

export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  name: "EduGenie",
  slug: "edugenie",
  extra: {
    apiUrl: process.env.API_URL ?? "https://api.edugenie.io",
    supabaseUrl: process.env.SUPABASE_URL,
    stripePublishableKey: process.env.STRIPE_PUBLISHABLE_KEY,
  },
});
