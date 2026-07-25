plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.dmoede.garytracker"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.dmoede.garytracker"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"
    }

    signingConfigs {
        // A fixed key committed to the repo so every build is signed
        // identically — lets installs update in place instead of failing
        // with "App not installed". Fine for a personal, non-Play-Store app.
        create("stable") {
            storeFile = file("gary-signing.keystore")
            storePassword = "garytracker"
            keyAlias = "gary"
            keyPassword = "garytracker"
        }
    }

    buildTypes {
        debug {
            signingConfig = signingConfigs.getByName("stable")
        }
        release {
            isMinifyEnabled = false
            signingConfig = signingConfigs.getByName("stable")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.15.0")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.google.android.material:material:1.12.0")
}
