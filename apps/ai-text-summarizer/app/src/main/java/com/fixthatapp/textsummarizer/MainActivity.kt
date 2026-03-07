package com.fixthatapp.textsummarizer

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.net.Uri
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
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

class MainActivity : AppCompatActivity() {

    private lateinit var textInput: EditText
    private lateinit var statsText: TextView
    private lateinit var resultText: TextView
    private lateinit var resultLabel: TextView
    private lateinit var summaryStats: TextView
    private lateinit var lengthGroup: RadioGroup
    private lateinit var btnSummarize: Button
    private lateinit var btnCopy: MaterialButton
    private lateinit var btnClear: MaterialButton
    private lateinit var adView: AdView

    private val stopWords = setOf(
        "the", "a", "an", "is", "are", "was", "were", "in", "on", "at",
        "to", "for", "of", "and", "or", "but", "not", "with", "this",
        "that", "it", "be", "has", "had", "have", "do", "does", "did",
        "will", "would", "could", "should", "may", "might"
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val toolbar = findViewById<MaterialToolbar>(R.id.toolbar)
        setSupportActionBar(toolbar)

        textInput = findViewById(R.id.textInput)
        statsText = findViewById(R.id.statsText)
        resultText = findViewById(R.id.resultText)
        resultLabel = findViewById(R.id.resultLabel)
        summaryStats = findViewById(R.id.summaryStats)
        lengthGroup = findViewById(R.id.lengthGroup)
        btnSummarize = findViewById(R.id.btnSummarize)
        btnCopy = findViewById(R.id.btnCopy)
        btnClear = findViewById(R.id.btnClear)
        adView = findViewById(R.id.adView)

        MobileAds.initialize(this) {}
        val adRequest = AdRequest.Builder().build()
        adView.loadAd(adRequest)

        textInput.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
            override fun afterTextChanged(s: Editable?) {
                val text = s?.toString()?.trim() ?: ""
                val wordCount = if (text.isEmpty()) 0 else text.split("\\s+".toRegex()).size
                val sentenceCount = countSentences(text)
                statsText.text = "$wordCount words | $sentenceCount sentences"
            }
        })

        btnSummarize.setOnClickListener {
            val text = textInput.text.toString().trim()
            if (text.isEmpty()) {
                Snackbar.make(textInput, "Please enter some text to summarize.", Snackbar.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            val summary = summarize(text)
            resultText.text = summary
            resultLabel.visibility = View.VISIBLE
            resultText.visibility = View.VISIBLE
            summaryStats.visibility = View.VISIBLE

            val originalWordCount = text.split("\\s+".toRegex()).size
            val summaryWordCount = if (summary.isEmpty()) 0 else summary.split("\\s+".toRegex()).size
            val reduction = if (originalWordCount > 0) {
                ((originalWordCount - summaryWordCount) * 100) / originalWordCount
            } else 0

            summaryStats.text = "Original: $originalWordCount words → Summary: $summaryWordCount words ($reduction% reduction)"
            summaryStats.setTextColor(Color.parseColor("#2E7D32"))
        }

        btnCopy.setOnClickListener {
            val summary = resultText.text.toString()
            if (summary.isNotEmpty()) {
                val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                val clip = ClipData.newPlainText("Summary", summary)
                clipboard.setPrimaryClip(clip)
                Snackbar.make(textInput, "Summary copied to clipboard!", Snackbar.LENGTH_SHORT).show()
            }
        }

        btnClear.setOnClickListener {
            textInput.text.clear()
            resultText.text = ""
            resultLabel.visibility = View.GONE
            resultText.visibility = View.GONE
            summaryStats.visibility = View.GONE
            summaryStats.text = ""
            statsText.text = "0 words | 0 sentences"
        }
    }

    private fun countSentences(text: String): Int {
        if (text.isEmpty()) return 0
        val sentences = splitIntoSentences(text)
        return sentences.size
    }

    private fun splitIntoSentences(text: String): List<String> {
        if (text.isBlank()) return emptyList()
        val sentences = text.split(Regex("(?<=[.!?])\\s+(?=[A-Z])|\\n+(?=[A-Z])"))
            .map { it.trim() }
            .filter { it.isNotBlank() }
        return if (sentences.isEmpty() && text.isNotBlank()) listOf(text) else sentences
    }

    private fun summarize(text: String): String {
        val sentences = splitIntoSentences(text)
        if (sentences.size <= 1) return text

        // Build word frequency map excluding stop words
        val wordFrequency = mutableMapOf<String, Int>()
        for (sentence in sentences) {
            val words = sentence.lowercase().split("\\s+".toRegex())
            for (word in words) {
                val cleaned = word.replace(Regex("[^a-zA-Z0-9]"), "").lowercase()
                if (cleaned.isNotEmpty() && cleaned !in stopWords) {
                    wordFrequency[cleaned] = (wordFrequency[cleaned] ?: 0) + 1
                }
            }
        }

        // Score each sentence by summing word frequencies
        val sentenceScores = sentences.mapIndexed { index, sentence ->
            val words = sentence.lowercase().split("\\s+".toRegex())
            val score = words.sumOf { word ->
                val cleaned = word.replace(Regex("[^a-zA-Z0-9]"), "").lowercase()
                wordFrequency[cleaned] ?: 0
            }
            Triple(index, sentence, score)
        }

        // Determine how many sentences to select based on length setting
        val ratio = when (lengthGroup.checkedRadioButtonId) {
            R.id.lengthShort -> 0.20
            R.id.lengthMedium -> 0.40
            R.id.lengthLong -> 0.60
            else -> 0.20
        }

        val minSentences = when (lengthGroup.checkedRadioButtonId) {
            R.id.lengthShort -> 1
            R.id.lengthMedium -> 2
            R.id.lengthLong -> 3
            else -> 1
        }

        val numToSelect = maxOf(minSentences, (sentences.size * ratio).toInt())
            .coerceAtMost(sentences.size)

        // Select top N sentences by score
        val topSentenceIndices = sentenceScores
            .sortedByDescending { it.third }
            .take(numToSelect)
            .map { it.first }
            .sorted() // Return in original order

        return topSentenceIndices.joinToString(" ") { sentences[it] }
    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menu?.add(0, 1, 0, "Privacy Policy")
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            1 -> {
                val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://fixthatapp.com/privacy"))
                startActivity(intent)
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }
}
