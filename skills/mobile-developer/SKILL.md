---
name: mobile-developer
description: >-
  Builds mobile apps in React Native, Flutter, or native Swift and Kotlin: screens,
  navigation, state, local storage, permissions, push, and platform integration. Use when
  the deliverable is an iOS or Android app or a mobile-specific bug. Desktop shells route
  to desktop-app-developer; shared web UI to frontend-web-engineer.
metadata:
  version: 3.0.0
  domain: delivery
  grade: G2
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: mobile-developer
---

# MOBILE DEVELOPER

Expert mobile development across native and cross-platform frameworks.

## REACT NATIVE

See `references/react-native.md` — component + navigation patterns. Load only for React Native tasks.

## FLUTTER / DART

See `references/flutter.md` — widget + Provider patterns. Load only for Flutter tasks.

## NATIVE ANDROID / KOTLIN

See `references/android-kotlin.md` — ViewModel + StateFlow pattern. Load only for native Android tasks.

## NATIVE IOS / SWIFT

See `references/ios-swift.md` — SwiftUI + ObservableObject pattern. Load only for native iOS tasks.

## CROSS-PLATFORM PATTERNS

### API Service
```dart
// Flutter
class ApiService {
  final String baseUrl;
  final http.Client client;
  
  ApiService({required this.baseUrl, http.Client? client})
      : client = client ?? http.Client();
  
  Future<T> get<T>(String endpoint, T Function(dynamic) fromJson) async {
    final response = await client.get(
      Uri.parse('$baseUrl$endpoint'),
      headers: {'Content-Type': 'application/json'},
    );
    
    if (response.statusCode == 200) {
      return fromJson(jsonDecode(response.body));
    }
    throw Exception('Failed to load');
  }
}
```

### Secure Storage
```kotlin
// Android - EncryptedSharedPreferences
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .build()

val secureStorage = EncryptedSharedPreferences.create(
    context,
    "secure_prefs",
    masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)
```

## OUTPUT
```text
[MOBILE DEV]
Framework: {React Native|Flutter|Swift|Kotlin}
Platform: {iOS|Android|Both}

DELIVERABLES:
- {component/view 1}
- {component/view 2}

PATTERNS:
- {pattern 1}
- {pattern 2}
```

## WHEN TO USE
- Building a screen, navigation flow, state layer, or platform integration in React Native, Flutter, native iOS (Swift/SwiftUI), or native Android (Kotlin).
- Choosing the right approach for a mobile UI/UX concern (list, navigation, secure storage, platform behavior).
- Porting or comparing the same feature across iOS/Android to keep behavior consistent and native.
- Adding platform integration (permissions, storage, push, background, biometrics) in a mobile app.

## WHEN NOT TO USE
- **A web/dashboard UI** — browser-only UI belongs to UI/UX skills, not mobile.
- **Backend or service code for the app** — the API, auth, and infra are devops/api design, not this.
- **Pure accessibility audit** of a mobile screen — accessibility-specialist handles the review; this skill implements the native solution.
- **Game-engine mobile work** — use the game-developer skill (Unity/Unreal/Godot); Roblox mobile work uses the `roblox-*` suite (`roblox-ui-designer` for touch-safe UI, `roblox-world-building` for device budgets).
- **One-line wrapper or a mocked prototype** — a throwaway scaffold doesn't need navigation and state-management decisions.

## DECISION TREE
```text
1. TARGET → iOS + Android both? React Native or Flutter (single codebase). iOS-only? Swift/SwiftUI.
   Android-only? Kotlin. Else → native per platform.
2. APP SHAPE → screens(): list, detail, forms → pick navigation (NativeStack / Navigator).
   State: local + server data → a state solution (Provider, Riverpod, Redux, Compose/SwiftUI state).
3. STORAGE → sensitive data → secure storage (Keychain/EncryptedSharedPreferences / flutter_secure_storage).
4. INTEGRATION → permissions, deep link, push — use the platform's canonical plugin/API.
5. VERIFY → run on device/simulator; check lifecycle/rotation/background; confirm no leaked privileges
   and behavior is native to each OS.
```
Never choose a cross-platform framework before knowing whether it must run on both OSes and how platform-native behavior matters.

## FAILURE MODES & MITIGATIONS
- **Wrong framework choice (native vs cross-platform).**
  DETECT: a React Native app can't reach a deep native API cleanly, or native-only is overkill adding two codebases.
  FIX: choose by target matrix + integration depth: one OS → native; both OSes + abundant native plugins → Flutter or RN; deep unique iOS+Android features → native.
- **Navigation state drift.**
  DETECT: back-stack or deep-link state goes inconsistent; a push replaces vs presents at the wrong level and the new screen doesn't stack correctly.
  FIX: use the canonical navigator, keep the stack type explicit (NativeStack vs presentation), and push in a consistent `rootNavigation` helper.
- **Unsecure storage.**
  DETECT: tokens/keys written to plain shared preferences / UserDefaults / local disk.
  FIX: use Keychain (iOS), EncryptedSharedPreferences / Keystore (Android), or flutter_secure_storage (cross) for secrets; never store auth in plain prefs.
- **Over-fetching / UI thread stalls.**
  DETECT: network calls or heavy parsing on the main thread; janky scroll, ANR, or "not responding" reports.
  FIX: move I/O off the main thread (async/await, coroutines, Combine), keep list building in a separate builder, and cache small responses.
- **Platform divergence (behavior differs between OS).**
  DETECT: the same interaction looks/behaves differently on iOS vs Android unexpectedly (keyboard, back, permissions).
  FIX: define a per-platform behavior layer, test both OSs in the verification gate, and document the intentional platform difference.
- **Lifecycle misuse (state lost on rotation/background).**
  DETECT: state is lost on rotation or process death because it lives only in the UI widget/Activity lifecycle.
  FIX: hoist persistent state outside the lifecycle (ViewModel/ViewModelProvider, Provider/Riverpod, @StateObject), or persist it; restore on recreation.

## VERIFICATION GATE
- **Builds on the target platform**: iOS/Android build and run; no deprecation/runtime errors in the new feature.
- **Lifecycle honored**: state survives rotation and background/foreground correctly (no lost screen state).
- **Permissions minimal**: only needed permissions requested, at the right moment, with a clear rationale.
- **Secure storage verified**: secrets are in Keychain/Keystore/flutter secure storage; no plain-text secrets on disk.
- **Platform behavior matched**: the feature behaves consistently or intentionally differently per the platform contract.
- **red-team-qa review**: adversarial check for insecure storage, main-thread stalls, or navigation/state loss.

## REFERENCES
- React Native documentation — components, navigation, async storage/security.
- Flutter documentation — widgets, state (Provider/Riverpod/Bloc), plugins.
- Apple Developer (SwiftUI, Keychain) and Android Developers (Kotlin, ViewModel, EncryptedSharedPreferences).
- OWASP MobileMASVS — secure data storage and platform integration guidance.
