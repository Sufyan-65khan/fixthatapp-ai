package com.fixthatapp.usernamegenerator

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
import android.widget.EditText
import android.widget.RadioGroup
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.google.android.gms.ads.AdRequest
import com.google.android.gms.ads.AdView
import com.google.android.gms.ads.MobileAds
import com.google.android.material.appbar.MaterialToolbar
import com.google.android.material.button.MaterialButton
import com.google.android.material.snackbar.Snackbar
import kotlin.random.Random

class MainActivity : AppCompatActivity() {

    private lateinit var keywordInput: EditText
    private lateinit var styleGroup: RadioGroup
    private lateinit var btnGenerate: Button
    private lateinit var resultLabel: TextView
    private lateinit var resultText: TextView
    private lateinit var btnCopy: MaterialButton
    private lateinit var btnClear: MaterialButton
    private lateinit var adView: AdView

    companion object {
        val coolAdjectives = listOf("Shadow", "Cyber", "Neo", "Dark", "Storm", "Blaze", "Frost", "Neon", "Phantom", "Apex")
        val coolNouns = listOf("Wolf", "Hawk", "Viper", "Knight", "Raven", "Phoenix", "Dragon", "Titan", "Ghost", "Ninja")
        val gamingWords = listOf("Sniper", "Striker", "Legend", "Elite", "Pro", "Boss", "King", "Master", "Chief", "Ace")
        val proAdjectives = listOf("Creative", "Digital", "Tech", "Smart", "Bright", "Swift", "Prime", "Core", "Meta", "Nova")
        val funnyAdjectives = listOf("Chunky", "Sneaky", "Wobbly", "Dizzy", "Goofy", "Quirky", "Zappy", "Fluffy", "Cranky", "Spicy")
        val funnyNouns = listOf("Potato", "Noodle", "Pickle", "Waffle", "Banana", "Taco", "Muffin", "Nugget", "Pancake", "Burrito")
        val aestheticWords = listOf("moon", "blossom", "starlight", "velvet", "crystal", "aurora", "dream", "petal", "misty", "serene")
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val toolbar = findViewById<MaterialToolbar>(R.id.toolbar)
        setSupportActionBar(toolbar)

        keywordInput = findViewById(R.id.keywordInput)
        styleGroup = findViewById(R.id.styleGroup)
        btnGenerate = findViewById(R.id.btnGenerate)
        resultLabel = findViewById(R.id.resultLabel)
        resultText = findViewById(R.id.resultText)
        btnCopy = findViewById(R.id.btnCopy)
        btnClear = findViewById(R.id.btnClear)
        adView = findViewById(R.id.adView)

        MobileAds.initialize(this) {}
        val adRequest = AdRequest.Builder().build()
        adView.loadAd(adRequest)

        btnGenerate.setOnClickListener {
            val selectedStyle = styleGroup.checkedRadioButtonId
            val keyword = keywordInput.text.toString().trim()
            val usernames = generateUsernames(selectedStyle, keyword)
            resultText.text = usernames.joinToString("\n")
            resultLabel.visibility = View.VISIBLE
            resultText.visibility = View.VISIBLE
        }

        btnCopy.setOnClickListener {
            val text = resultText.text.toString()
            if (text.isNotEmpty()) {
                val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                val clip = ClipData.newPlainText("Usernames", text)
                clipboard.setPrimaryClip(clip)
                Snackbar.make(it, "Usernames copied to clipboard!", Snackbar.LENGTH_SHORT).show()
            } else {
                Snackbar.make(it, "Nothing to copy. Generate usernames first!", Snackbar.LENGTH_SHORT).show()
            }
        }

        btnClear.setOnClickListener {
            keywordInput.text.clear()
            styleGroup.check(R.id.radioCool)
            resultLabel.visibility = View.GONE
            resultText.visibility = View.GONE
            resultText.text = ""
        }
    }

    private fun generateUsernames(style: Int, keyword: String): List<String> {
        val usernames = mutableListOf<String>()

        for (i in 1..10) {
            val username = when (style) {
                R.id.radioCool -> {
                    val adj = coolAdjectives.random()
                    val noun = coolNouns.random()
                    val num = Random.nextInt(10, 99)
                    if (keyword.isNotEmpty() && Random.nextBoolean()) {
                        "${adj}${keyword.replaceFirstChar { it.uppercase() }}$num"
                    } else {
                        "$adj$noun$num"
                    }
                }

                R.id.radioGaming -> {
                    val word1 = gamingWords.random()
                    val word2 = gamingWords.random()
                    val num = Random.nextInt(1, 999)
                    val separator = if (Random.nextBoolean()) "x" else "_"
                    if (keyword.isNotEmpty() && Random.nextBoolean()) {
                        "${keyword.replaceFirstChar { it.uppercase() }}${separator}${word1}$num"
                    } else {
                        "${word1}${separator}${word2}$num"
                    }
                }

                R.id.radioProfessional -> {
                    val adj = proAdjectives.random()
                    val num = Random.nextInt(1, 99)
                    if (keyword.isNotEmpty()) {
                        "${keyword.replaceFirstChar { it.uppercase() }}${adj}$num"
                    } else {
                        "${adj}${coolNouns.random()}$num"
                    }
                }

                R.id.radioFunny -> {
                    val adj = funnyAdjectives.random()
                    val noun = funnyNouns.random()
                    val num = Random.nextInt(1, 999)
                    if (keyword.isNotEmpty() && Random.nextBoolean()) {
                        "${adj}${keyword.replaceFirstChar { it.uppercase() }}$num"
                    } else {
                        "$adj$noun$num"
                    }
                }

                R.id.radioAesthetic -> {
                    val word1 = aestheticWords.random()
                    val word2 = aestheticWords.random()
                    val num = Random.nextInt(0, 99)
                    if (keyword.isNotEmpty() && Random.nextBoolean()) {
                        "${keyword.lowercase()}_${word1}_$num"
                    } else {
                        "${word1}_${word2}_$num"
                    }
                }

                else -> "user${Random.nextInt(1000, 9999)}"
            }
            usernames.add(username)
        }

        return usernames
    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menu?.add(0, 1, 0, "Privacy Policy")
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
