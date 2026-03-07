"""Generate Android project boilerplate for all apps."""
import os

APPS = {
    "json-formatter": {"name": "JSON Formatter", "pkg": "jsonformatter", "theme": "JsonFormatter"},
    "text-case-converter": {"name": "Text Case Converter", "pkg": "caseconverter", "theme": "CaseConverter"},
    "username-generator": {"name": "Username Generator", "pkg": "usernamegenerator", "theme": "UsernameGenerator"},
    "ai-text-summarizer": {"name": "AI Text Summarizer", "pkg": "textsummarizer", "theme": "TextSummarizer"},
    "regex-tester": {"name": "Regex Tester", "pkg": "regextester", "theme": "RegexTester"},
    "markdown-previewer": {"name": "Markdown Previewer", "pkg": "markdownpreviewer", "theme": "MarkdownPreviewer"},
    "error-message-explainer": {"name": "Error Message Explainer", "pkg": "errorexplainer", "theme": "ErrorExplainer"},
}

PRIVACY_BASE = """Privacy Policy\\n\\nLast updated: March 5, 2026\\n\\n{name} by FixThatApp\\n\\nThis app processes all data entirely on your device. No data is stored, transmitted, or collected by us.\\n\\nData Collection:\\nWe do not collect any personal data. The app works completely offline.\\n\\nAdvertising:\\nThis app uses Google AdMob to display advertisements. AdMob may collect device identifiers and usage data to serve relevant ads. You can learn more at https://policies.google.com/privacy\\n\\nThird-Party Services:\\n\\u2022 Google AdMob (advertising)\\n\\nChildren\\'s Privacy:\\nThis app is not intended for children under 13.\\n\\nContact:\\nFor questions, contact us at sufyankhan65@gmail.com\\n\\nPublisher: FixThatApp\\nWebsite: www.fixthatapp.com"""

for folder, info in APPS.items():
    base = f"apps/{folder}"
    pkg = info["pkg"]
    name = info["name"]
    theme = info["theme"]

    dirs = [
        f"{base}/app/src/main/java/com/fixthatapp/{pkg}",
        f"{base}/app/src/main/res/layout",
        f"{base}/app/src/main/res/values",
        f"{base}/app/src/main/res/values-night",
        f"{base}/app/src/main/res/menu",
        f"{base}/gradle/wrapper",
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # settings.gradle.kts
    with open(f"{base}/settings.gradle.kts", "w") as f:
        f.write(f'''pluginManagement {{
    repositories {{
        google()
        mavenCentral()
        gradlePluginPortal()
    }}
}}
dependencyResolution {{
    repositories {{
        google()
        mavenCentral()
    }}
}}
rootProject.name = "{name.replace(" ", "")}"
include(":app")
''')

    # build.gradle.kts (project)
    with open(f"{base}/build.gradle.kts", "w") as f:
        f.write('''plugins {
    id("com.android.application") version "8.2.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.22" apply false
}
''')

    # app/build.gradle.kts
    with open(f"{base}/app/build.gradle.kts", "w") as f:
        f.write(f'''plugins {{
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}}

android {{
    namespace = "com.fixthatapp.{pkg}"
    compileSdk = 34

    defaultConfig {{
        applicationId = "com.fixthatapp.{pkg}"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }}

    buildTypes {{
        release {{
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }}
    }}

    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }}

    kotlinOptions {{
        jvmTarget = "1.8"
    }}
}}

dependencies {{
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.11.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    implementation("com.google.android.gms:play-services-ads:23.0.0")
}}
''')

    # gradle.properties
    with open(f"{base}/gradle.properties", "w") as f:
        f.write('''org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
''')

    # AndroidManifest.xml
    with open(f"{base}/app/src/main/AndroidManifest.xml", "w") as f:
        f.write(f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.{theme}">

        <meta-data
            android:name="com.google.android.gms.ads.APPLICATION_ID"
            android:value="ca-app-pub-3940256099942544~3347511713" />

        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <activity android:name=".PrivacyPolicyActivity" android:exported="false"
            android:label="@string/privacy_policy" />
    </application>
</manifest>
''')

    # PrivacyPolicyActivity.kt
    with open(f"{base}/app/src/main/java/com/fixthatapp/{pkg}/PrivacyPolicyActivity.kt", "w") as f:
        f.write(f'''package com.fixthatapp.{pkg}

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class PrivacyPolicyActivity : AppCompatActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_privacy_policy)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.title = "Privacy Policy"
    }}

    override fun onSupportNavigateUp(): Boolean {{
        finish()
        return true
    }}
}}
''')

    # activity_privacy_policy.xml
    with open(f"{base}/app/src/main/res/layout/activity_privacy_policy.xml", "w") as f:
        f.write('''<?xml version="1.0" encoding="utf-8"?>
<ScrollView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="?android:colorBackground"
    android:padding="24dp">
    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="@string/privacy_policy_text"
        android:textSize="14sp"
        android:lineSpacingMultiplier="1.5"
        android:textColor="?android:textColorPrimary" />
</ScrollView>
''')

    # colors.xml
    with open(f"{base}/app/src/main/res/values/colors.xml", "w") as f:
        f.write('''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="purple_primary">#667EEA</color>
    <color name="purple_dark">#5A6FD6</color>
    <color name="purple_light">#8B9CF7</color>
    <color name="code_bg">#F0F0F5</color>
    <color name="white">#FFFFFF</color>
    <color name="black">#000000</color>
</resources>
''')

    # themes.xml
    with open(f"{base}/app/src/main/res/values/themes.xml", "w") as f:
        f.write(f'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.{theme}" parent="Theme.Material3.Light.NoActionBar">
        <item name="colorPrimary">@color/purple_primary</item>
        <item name="colorPrimaryDark">@color/purple_dark</item>
        <item name="colorAccent">@color/purple_primary</item>
    </style>
</resources>
''')

    # values-night/themes.xml
    with open(f"{base}/app/src/main/res/values-night/themes.xml", "w") as f:
        f.write(f'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.{theme}" parent="Theme.Material3.Dark.NoActionBar">
        <item name="colorPrimary">@color/purple_light</item>
        <item name="colorPrimaryDark">@color/purple_dark</item>
        <item name="colorAccent">@color/purple_light</item>
    </style>
</resources>
''')

    # menu/main_menu.xml
    with open(f"{base}/app/src/main/res/menu/main_menu.xml", "w") as f:
        f.write('''<?xml version="1.0" encoding="utf-8"?>
<menu xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto">
    <item android:id="@+id/action_privacy" android:title="@string/privacy_policy"
        app:showAsAction="never" />
</menu>
''')

    # strings.xml
    privacy_text = PRIVACY_BASE.format(name=name)
    with open(f"{base}/app/src/main/res/values/strings.xml", "w") as f:
        f.write(f'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{name}</string>
    <string name="privacy_policy">Privacy Policy</string>
    <string name="privacy_policy_text">{privacy_text}</string>
</resources>
''')

    print(f"Created boilerplate for: {name}")

print("\nDone! All 7 app boilerplates generated.")
