package com.fixthatapp.passwordgenerator

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
import com.google.android.material.slider.Slider
import com.google.android.material.snackbar.Snackbar
import java.security.SecureRandom

class MainActivity : AppCompatActivity() {

    private lateinit var passwordText: TextView
    private lateinit var lengthSlider: Slider
    private lateinit var lengthLabel: TextView
    private lateinit var cbUpper: CheckBox
    private lateinit var cbLower: CheckBox
    private lateinit var cbNumbers: CheckBox
    private lateinit var cbSymbols: CheckBox
    private lateinit var strengthBar: ProgressBar
    private lateinit var strengthLabel: TextView

    private val random = SecureRandom()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setSupportActionBar(findViewById(R.id.toolbar))

        MobileAds.initialize(this)
        val adView: AdView = findViewById(R.id.adView)
        adView.loadAd(AdRequest.Builder().build())

        passwordText = findViewById(R.id.passwordText)
        lengthSlider = findViewById(R.id.lengthSlider)
        lengthLabel = findViewById(R.id.lengthLabel)
        cbUpper = findViewById(R.id.cbUppercase)
        cbLower = findViewById(R.id.cbLowercase)
        cbNumbers = findViewById(R.id.cbNumbers)
        cbSymbols = findViewById(R.id.cbSymbols)
        strengthBar = findViewById(R.id.strengthBar)
        strengthLabel = findViewById(R.id.strengthLabel)

        lengthSlider.addOnChangeListener { _, value, _ ->
            lengthLabel.text = "Length: ${value.toInt()}"
        }

        findViewById<Button>(R.id.btnGenerate).setOnClickListener { generate() }
        findViewById<Button>(R.id.btnCopy).setOnClickListener { copyPassword() }

        generate()
    }

    private fun generate() {
        val length = lengthSlider.value.toInt()
        var chars = ""
        if (cbUpper.isChecked) chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if (cbLower.isChecked) chars += "abcdefghijklmnopqrstuvwxyz"
        if (cbNumbers.isChecked) chars += "0123456789"
        if (cbSymbols.isChecked) chars += "!@#\$%^&*()_+-=[]{}|;:,.<>?"

        if (chars.isEmpty()) {
            Toast.makeText(this, "Select at least one character type", Toast.LENGTH_SHORT).show()
            return
        }

        val password = StringBuilder()
        for (i in 0 until length) {
            password.append(chars[random.nextInt(chars.length)])
        }

        val pw = password.toString()
        passwordText.text = pw
        updateStrength(pw)
    }

    private fun updateStrength(pw: String) {
        var score = 0
        if (pw.length >= 8) score++
        if (pw.length >= 12) score++
        if (pw.length >= 16) score++
        if (pw.contains(Regex("[a-z]")) && pw.contains(Regex("[A-Z]"))) score++
        if (pw.contains(Regex("[0-9]"))) score++
        if (pw.contains(Regex("[^a-zA-Z0-9]"))) score++

        val level = score.coerceAtMost(5)
        val labels = arrayOf("Very Weak", "Weak", "Fair", "Good", "Strong", "Very Strong")
        val colors = arrayOf(0xFFE74C3C.toInt(), 0xFFE67E22.toInt(), 0xFFF39C12.toInt(),
            0xFF27AE60.toInt(), 0xFF2ECC71.toInt(), 0xFF00B894.toInt())

        strengthBar.progress = (level + 1) * 100 / 6
        strengthLabel.text = "Strength: ${labels[level]}"
        strengthLabel.setTextColor(colors[level])
    }

    private fun copyPassword() {
        val pw = passwordText.text.toString()
        if (pw.isBlank()) return
        val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        clipboard.setPrimaryClip(ClipData.newPlainText("password", pw))
        Snackbar.make(passwordText, "Password copied!", Snackbar.LENGTH_SHORT).show()
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
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
