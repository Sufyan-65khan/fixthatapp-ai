package com.fixthatapp.caseconverter

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.google.android.gms.ads.AdRequest
import com.google.android.gms.ads.AdView
import com.google.android.gms.ads.MobileAds
import com.google.android.material.snackbar.Snackbar

class MainActivity : AppCompatActivity() {

    private lateinit var textInput: EditText
    private lateinit var statusText: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        setSupportActionBar(findViewById(R.id.toolbar))

        MobileAds.initialize(this) {}

        val adView: AdView = findViewById(R.id.adView)
        val adRequest = AdRequest.Builder().build()
        adView.loadAd(adRequest)

        textInput = findViewById(R.id.textInput)
        statusText = findViewById(R.id.statusText)

        findViewById<Button>(R.id.btnUppercase).setOnClickListener { convertText("UPPERCASE") { it.uppercase() } }
        findViewById<Button>(R.id.btnLowercase).setOnClickListener { convertText("lowercase") { it.lowercase() } }
        findViewById<Button>(R.id.btnTitleCase).setOnClickListener { convertText("Title Case") { toTitleCase(it) } }
        findViewById<Button>(R.id.btnSentenceCase).setOnClickListener { convertText("Sentence case") { toSentenceCase(it) } }
        findViewById<Button>(R.id.btnCamelCase).setOnClickListener { convertText("camelCase") { toCamelCase(it) } }
        findViewById<Button>(R.id.btnPascalCase).setOnClickListener { convertText("PascalCase") { toPascalCase(it) } }
        findViewById<Button>(R.id.btnSnakeCase).setOnClickListener { convertText("snake_case") { toSnakeCase(it) } }
        findViewById<Button>(R.id.btnKebabCase).setOnClickListener { convertText("kebab-case") { toKebabCase(it) } }
        findViewById<Button>(R.id.btnConstantCase).setOnClickListener { convertText("CONSTANT_CASE") { toConstantCase(it) } }
        findViewById<Button>(R.id.btnDotCase).setOnClickListener { convertText("dot.case") { toDotCase(it) } }
        findViewById<Button>(R.id.btnToggleCase).setOnClickListener { convertText("tOgGlE cAsE") { toToggleCase(it) } }
        findViewById<Button>(R.id.btnReverse).setOnClickListener { convertText("Reverse") { it.reversed() } }

        findViewById<Button>(R.id.btnCopy).setOnClickListener {
            val text = textInput.text.toString()
            val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
            val clip = ClipData.newPlainText("Converted Text", text)
            clipboard.setPrimaryClip(clip)
            Snackbar.make(textInput, "Copied!", Snackbar.LENGTH_SHORT).show()
        }

        findViewById<Button>(R.id.btnClear).setOnClickListener {
            textInput.setText("")
            statusText.text = ""
        }
    }

    private fun convertText(caseName: String, converter: (String) -> String) {
        try {
            val text = textInput.text.toString()
            val result = converter(text)
            textInput.setText(result)
            statusText.text = "Converted to $caseName!"
            statusText.setTextColor(0xFF27AE60.toInt())
        } catch (e: Exception) {
            statusText.text = "Error converting to $caseName"
            statusText.setTextColor(0xFFE74C3C.toInt())
        }
    }

    private fun splitWords(text: String): List<String> {
        return text.split(Regex("[\\s_\\-]+")).filter { it.isNotEmpty() }
    }

    private fun toTitleCase(text: String): String {
        return text.split(" ").joinToString(" ") { word ->
            word.lowercase().replaceFirstChar { it.uppercase() }
        }
    }

    private fun toSentenceCase(text: String): String {
        return text.lowercase().split(Regex("(?<=[.!?])\\s+")).joinToString(" ") { sentence ->
            sentence.replaceFirstChar { it.uppercase() }
        }
    }

    private fun toCamelCase(text: String): String {
        val words = splitWords(text)
        if (words.isEmpty()) return text
        return words.first().lowercase() + words.drop(1).joinToString("") { word ->
            word.lowercase().replaceFirstChar { it.uppercase() }
        }
    }

    private fun toPascalCase(text: String): String {
        val words = splitWords(text)
        if (words.isEmpty()) return text
        return words.joinToString("") { word ->
            word.lowercase().replaceFirstChar { it.uppercase() }
        }
    }

    private fun toSnakeCase(text: String): String {
        return splitWords(text).joinToString("_") { it.lowercase() }
    }

    private fun toKebabCase(text: String): String {
        return splitWords(text).joinToString("-") { it.lowercase() }
    }

    private fun toConstantCase(text: String): String {
        return splitWords(text).joinToString("_") { it.uppercase() }
    }

    private fun toDotCase(text: String): String {
        return splitWords(text).joinToString(".") { it.lowercase() }
    }

    private fun toToggleCase(text: String): String {
        return text.mapIndexed { index, char ->
            if (index % 2 == 0) char.lowercase() else char.uppercase()
        }.joinToString("")
    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.main_menu, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_privacy -> {
                startActivity(Intent(this, PrivacyPolicyActivity::class.java))
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }
}
