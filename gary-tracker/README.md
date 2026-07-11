# Gary Tracker 🐾

A tiny Android app for Gary the vizsla (born May 6, 2026) with a home-screen
widget showing his current age and latest weight.

## Features

- **Age counter** — weeks + days while he's a puppy, then months, then years.
  Computed from his birthday, so it's always current.
- **Weight log** — enter a weight in lbs; entries are saved on-device
  (one per day, newest shown first, with the change from the previous
  weigh-in). Long-press an entry to delete it.
- **Home-screen widget** — shows Gary's age and most recent weight, refreshes
  itself periodically, and updates immediately when you log a weight. Tap it
  to open the app.

## Installing on your phone

1. Go to the repo's **Actions** tab → **Build Gary Tracker APK** → latest run.
2. Download the `gary-tracker-apk` artifact and unzip it to get
   `gary-tracker-gary.apk`.
3. Copy the APK to your phone (or download it there directly) and open it.
   Android will ask you to allow installing from unknown sources — allow it
   for the browser/files app you used.
4. Open **Gary** once, then long-press your home screen → *Widgets* → **Gary**
   and drag the widget wherever you like.

## Building locally

Requires the Android SDK (or just open the `gary-tracker` folder in Android
Studio):

```
cd gary-tracker
./gradlew assembleDebug
# APK lands in app/build/outputs/apk/debug/app-debug.apk
```
