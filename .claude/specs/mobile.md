# Mobile Application — EduGenie OS

## Overview

- **Framework:** React Native + Expo SDK 52+
- **Development:** Expo Go for daily testing, EAS Build for production builds
- **Platforms:** iOS and Android
- **Navigation:** React Navigation (stack, tab, drawer)
- **State Management:** Zustand (client state) + TanStack Query (server state)
- **Push Notifications:** Expo Push Notifications + Firebase Cloud Messaging

---

## Expo Configuration

### app.json
```json
{
  "expo": {
    "name": "EduGenie",
    "slug": "edugenie",
    "version": "1.0.0",
    "orientation": "portrait",
    "scheme": "edugenie",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "light",
    "splash": { "backgroundColor": "#2563EB" },
    "assetBundlePatterns": ["**/*"],
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "io.edugenie.learnspace",
      "associatedDomains": ["applinks:learn.edugenie.io"],
      "infoPlist": {
        "NSCameraUsageDescription": "Upload profile photo",
        "NSPhotoLibraryUsageDescription": "Save certificate to gallery"
      }
    },
    "android": {
      "package": "io.edugenie.learnspace",
      "intentFilters": [
        {
          "action": "VIEW",
          "autoVerify": true,
          "data": [{ "scheme": "https", "host": "*.edugenie.io" }],
          "category": ["BROWSABLE", "DEFAULT"]
        }
      ]
    },
    "plugins": [
      "expo-router",
      "expo-secure-store",
      "@stripe/stripe-react-native",
      "expo-notifications",
      "expo-linking"
    ],
    "extra": {
      "apiUrl": "https://api.edugenie.io",
      "supabaseUrl": "https://xxx.supabase.co",
      "stripePublishableKey": "pk_live_..."
    }
  }
}
```

---

## Navigation Structure

```
RootNavigator (Stack)
├── AuthStack
│   ├── Login
│   ├── Signup
│   └── MagicLink
├── MainTabs (Tab Navigator)
│   ├── LearnStack
│   │   ├── MyCourses
│   │   ├── CoursePlayer
│   │   └── QuizScreen
│   ├── MarketplaceStack
│   │   ├── Browse
│   │   ├── Search
│   │   └── CourseDetail
│   └── ProfileStack
│       ├── Profile
│       ├── Certificates
│       └── Settings
└── NotificationStack
    └── NotificationCenter
```

### Key Files
- `mobile-app/src/navigation/RootNavigator.tsx` — Top-level stack navigator
- `mobile-app/App.tsx` — App entry, wraps navigation with providers

---

## Push Notifications (Expo + FCM)

### Setup
```typescript
// mobile-app/src/services/notifications.ts
import * as Notifications from 'expo-notifications';

export async function registerForPushNotifications() {
  const { status } = await Notifications.requestPermissionsAsync();
  if (status !== 'granted') return null;
  const token = await Notifications.getExpoPushTokenAsync();
  // POST /api/v1/notifications/register-push-token { token, platform }
  return token;
}

// Handle notification tap → deep link
Notifications.addNotificationResponseReceivedListener((response) => {
  const { courseId, screen } = response.notification.request.content.data;
  // Navigate: router.push(`/learn/${courseId}`)
});
```

### Notification Types
- Course update available
- Certificate earned
- New discussion reply
- Enrollment confirmed
- Reminder to continue course

---

## Stripe SDK Integration

| Platform | SDK | Payment Methods |
|----------|-----|-----------------|
| **Web** | `@stripe/react-stripe-js` | Card, Apple Pay, Google Pay |
| **Mobile** | `@stripe/stripe-react-native` | Apple Pay (iOS), Google Pay (Android), Cards |
| **Backend** | Stripe Python SDK | Checkout Sessions, Payment Intents, PaymentSheet |

### Mobile Checkout Flow
```
1. User taps "Buy" → backend creates PaymentSheet
2. Backend returns ephemeralKey + paymentIntent + customer
3. Mobile opens Stripe PaymentSheet
4. User completes payment → Stripe confirms
5. Backend webhook: checkout.session.completed → enroll student
```

---

## EAS Build Configuration

### eas.json
```json
{
  "cli": { "version": ">= 3.0" },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "channel": "development",
      "env": {
        "API_URL": "https://api-staging.edugenie.io",
        "SUPABASE_URL": "https://xxx.supabase.co"
      }
    },
    "preview": {
      "distribution": "internal",
      "channel": "staging",
      "android": { "buildType": "apk" },
      "ios": { "simulator": true }
    },
    "production": {
      "channel": "production",
      "env": {
        "API_URL": "https://api.edugenie.io",
        "SUPABASE_URL": "https://xxx.supabase.co"
      }
    }
  },
  "submit": {
    "production": {
      "ios": { "appleId": "...", "ascAppId": "..." },
      "android": { "track": "production", "releaseStatus": "completed" }
    }
  }
}
```

### Build Commands
```bash
# Development build (internal testing)
eas build --platform all --profile development

# Preview build (QA)
eas build --platform all --profile preview

# Production
eas build --platform all --profile production
eas submit --platform ios --profile production
eas submit --platform android --profile production
```

---

## Testing Strategy

| Method | Tool | Scope |
|--------|------|-------|
| Daily dev testing | Expo Go | Physical devices, rapid iteration |
| Unit tests | Jest + React Native Testing Library | Components, hooks, services |
| Beta distribution (iOS) | EAS Build + TestFlight | QA team |
| Internal track (Android) | EAS Build + Google Play Console | QA team |
| E2E UI tests | Detox / Maestro | Critical flows: enrollment, quiz, certificate |

---

## Directory Structure
```
mobile-app/
├── app.json                    # Expo config
├── app.config.ts
├── package.json
├── tsconfig.json
├── babel.config.js
├── eas.json                    # EAS Build config
├── App.tsx
└── src/
    ├── navigation/
    │   └── RootNavigator.tsx
    ├── screens/
    │   ├── auth/               # Login, Signup, MagicLink
    │   ├── learnspace/         # MyCourses, CoursePlayer, QuizScreen
    │   ├── marketplace/        # Browse, Search, CourseDetail
    │   └── profile/            # Profile, Certificates, Settings
    ├── components/             # Shared UI components
    ├── services/
    │   ├── api.ts              # Axios client
    │   ├── auth.ts             # Supabase auth helpers
    │   └── notifications.ts   # Push notification registration
    ├── hooks/                  # Custom hooks
    ├── store/                  # Zustand stores
    └── utils/                  # Helper functions
```
