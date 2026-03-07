package com.fixthatapp.regextester

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.widget.Button
import android.widget.CheckBox
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.google.android.gms.ads.AdRequest
import com.google.android.gms.ads.AdView
import com.google.android.gms.ads.MobileAds
import com.google.android.material.appbar.MaterialToolbar
import java.util.regex.PatternSyntaxException

class MainActivity : AppCompatActivity() {

    private lateinit var regexInput: EditText
    private lateinit var testInput: EditText
    private lateinit var resultText: TextView
    private lateinit var resultLabel: TextView
    private lateinit var flagIgnoreCase: CheckBox
    private lateinit var flagMultiline: CheckBox
    private lateinit var flagDotAll: CheckBox
    private lateinit var adView: AdView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val toolbar = findViewById<MaterialToolbar>(R.id.toolbar)
        setSupportActionBar(toolbar)

        regexInput = findViewById(R.id.regexInput)
        testInput = findViewById(R.id.testInput)
        resultText = findViewById(R.id.resultText)
        resultLabel = findViewById(R.id.resultLabel)
        flagIgnoreCase = findViewById(R.id.flagIgnoreCase)
        flagMultiline = findViewById(R.id.flagMultiline)
        flagDotAll = findViewById(R.id.flagDotAll)

        val btnTest = findViewById<Button>(R.id.btnTest)
        val btnPresetEmail = findViewById<Button>(R.id.btnPresetEmail)
        val btnPresetUrl = findViewById<Button>(R.id.btnPresetUrl)
        val btnPresetPhone = findViewById<Button>(R.id.btnPresetPhone)
        val btnCopy = findViewById<Button>(R.id.btnCopy)
        val btnClear = findViewById<Button>(R.id.btnClear)

        btnTest.setOnClickListener { testRegex() }

        btnPresetEmail.setOnClickListener {
            regexInput.setText("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}")
        }

        btnPresetUrl.setOnClickListener {
            regexInput.setText("https?://[\\w\\-._~:/?#\\[\\]@!\$&'()*+,;=]+")
        }

        btnPresetPhone.setOnClickListener {
            regexInput.setText("\\+?\\d{1,3}[-.\\s]?\\(?\\d{1,4}\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}")
        }

        btnCopy.setOnClickListener {
            val text = resultText.text.toString()
            if (text.isNotEmpty()) {
                val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                val clip = ClipData.newPlainText("Regex Result", text)
                clipboard.setPrimaryClip(clip)
                Toast.makeText(this, "Copied to clipboard", Toast.LENGTH_SHORT).show()
            }
        }

        btnClear.setOnClickListener {
            regexInput.text.clear()
            testInput.text.clear()
            resultText.text = ""
            resultLabel.visibility = View.GONE
            resultText.visibility = View.GONE
        }

        // Initialize Mobile Ads
        MobileAds.initialize(this) {}

        adView = findViewById(R.id.adView)
        val adRequest = AdRequest.Builder().build()
        adView.loadAd(adRequest)
    }

    private fun testRegex() {
        val pattern = regexInput.text.toString()
        val testString = testInput.text.toString()

        if (pattern.isEmpty()) {
            Toast.makeText(this, "Please enter a regex pattern", Toast.LENGTH_SHORT).show()
            return
        }

        if (testString.isEmpty()) {
            Toast.makeText(this, "Please enter a test string", Toast.LENGTH_SHORT).show()
            return
        }

        try {
            val options = mutableSetOf<RegexOption>()
            if (flagIgnoreCase.isChecked) options.add(RegexOption.IGNORE_CASE)
            if (flagMultiline.isChecked) options.add(RegexOption.MULTILINE)
            if (flagDotAll.isChecked) options.add(RegexOption.DOT_MATCHES_ALL)

            val regex = Regex(pattern, options)
            val matches = regex.findAll(testString).toList()

            resultLabel.visibility = View.VISIBLE
            resultText.visibility = View.VISIBLE

            if (matches.isNotEmpty()) {
                val sb = StringBuilder()
                sb.appendLine("Matches found: ${matches.size}")
                sb.appendLine("─".repeat(30))

                matches.forEachIndexed { index, match ->
                    sb.appendLine("Match ${index + 1}:")
                    sb.appendLine("  Value: \"${match.value}\"")
                    sb.appendLine("  Range: ${match.range.first}..${match.range.last}")
                    if (match.groupValues.size > 1) {
                        match.groupValues.forEachIndexed { groupIndex, group ->
                            if (groupIndex > 0) {
                                sb.appendLine("  Group $groupIndex: \"$group\"")
                            }
                        }
                    }
                    sb.appendLine()
                }

                resultText.text = sb.toString().trimEnd()
                resultText.setTextColor(ContextCompat.getColor(this, R.color.status_green))
            } else {
                resultText.text = "No matches found."
                resultText.setTextColor(ContextCompat.getColor(this, R.color.status_red))
            }
        } catch (e: PatternSyntaxException) {
            resultLabel.visibility = View.VISIBLE
            resultText.visibility = View.VISIBLE
            resultText.text = "Invalid regex pattern:\n${e.message}"
            resultText.setTextColor(ContextCompat.getColor(this, R.color.status_red))
        }
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menu.add(0, 1, 0, "Privacy Policy")
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            1 -> {
                val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://fixthatapp.com/privacy-policy"))
                startActivity(intent)
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }
}
