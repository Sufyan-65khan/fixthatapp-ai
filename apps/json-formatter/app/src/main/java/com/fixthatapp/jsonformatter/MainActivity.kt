package com.fixthatapp.jsonformatter

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import com.google.android.gms.ads.AdRequest
import com.google.android.gms.ads.AdView
import com.google.android.gms.ads.MobileAds
import com.google.android.material.snackbar.Snackbar
import org.json.JSONArray
import org.json.JSONObject
import org.json.JSONTokener

class MainActivity : AppCompatActivity() {

    private lateinit var jsonInput: EditText
    private lateinit var statusText: TextView
    private lateinit var statsText: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setSupportActionBar(findViewById(R.id.toolbar))

        MobileAds.initialize(this)
        findViewById<AdView>(R.id.adView).loadAd(AdRequest.Builder().build())

        jsonInput = findViewById(R.id.jsonInput)
        statusText = findViewById(R.id.statusText)
        statsText = findViewById(R.id.statsText)

        jsonInput.addTextChangedListener(object : android.text.TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
            override fun afterTextChanged(s: android.text.Editable?) { updateStats() }
        })

        findViewById<Button>(R.id.btnFormat).setOnClickListener { formatJson() }
        findViewById<Button>(R.id.btnMinify).setOnClickListener { minifyJson() }
        findViewById<Button>(R.id.btnValidate).setOnClickListener { validateJson() }
        findViewById<Button>(R.id.btnCopy).setOnClickListener { copyText() }
        findViewById<Button>(R.id.btnClear).setOnClickListener {
            jsonInput.setText("")
            statusText.text = ""
        }
    }

    private fun parseJson(text: String): Any {
        val trimmed = text.trim()
        val tokener = JSONTokener(trimmed)
        return tokener.nextValue()
    }

    private fun formatJson() {
        try {
            val obj = parseJson(jsonInput.text.toString())
            val formatted = when (obj) {
                is JSONObject -> obj.toString(2)
                is JSONArray -> obj.toString(2)
                else -> obj.toString()
            }
            jsonInput.setText(formatted)
            statusText.setTextColor(0xFF27AE60.toInt())
            statusText.text = "Valid JSON — formatted!"
        } catch (e: Exception) {
            statusText.setTextColor(0xFFE74C3C.toInt())
            statusText.text = "Error: ${e.message}"
        }
    }

    private fun minifyJson() {
        try {
            val obj = parseJson(jsonInput.text.toString())
            val minified = when (obj) {
                is JSONObject -> obj.toString()
                is JSONArray -> obj.toString()
                else -> obj.toString()
            }
            jsonInput.setText(minified)
            statusText.setTextColor(0xFF27AE60.toInt())
            statusText.text = "JSON minified!"
        } catch (e: Exception) {
            statusText.setTextColor(0xFFE74C3C.toInt())
            statusText.text = "Error: ${e.message}"
        }
    }

    private fun validateJson() {
        try {
            parseJson(jsonInput.text.toString())
            statusText.setTextColor(0xFF27AE60.toInt())
            statusText.text = "Valid JSON!"
        } catch (e: Exception) {
            statusText.setTextColor(0xFFE74C3C.toInt())
            statusText.text = "Invalid: ${e.message}"
        }
    }

    private fun updateStats() {
        val text = jsonInput.text.toString()
        val chars = text.length
        val lines = if (text.isEmpty()) 0 else text.lines().size
        statsText.text = "$chars chars | $lines lines | ${text.toByteArray().size} bytes"
    }

    private fun copyText() {
        val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        clipboard.setPrimaryClip(ClipData.newPlainText("json", jsonInput.text.toString()))
        Snackbar.make(jsonInput, "Copied!", Snackbar.LENGTH_SHORT).show()
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.main_menu, menu); return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        if (item.itemId == R.id.action_privacy) {
            startActivity(Intent(this, PrivacyPolicyActivity::class.java)); return true
        }
        return super.onOptionsItemSelected(item)
    }
}
