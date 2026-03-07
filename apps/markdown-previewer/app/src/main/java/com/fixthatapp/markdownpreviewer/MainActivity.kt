package com.fixthatapp.markdownpreviewer

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.webkit.WebView
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.gms.ads.AdRequest
import com.google.android.gms.ads.AdView
import com.google.android.gms.ads.MobileAds
import com.google.android.material.appbar.MaterialToolbar
import com.google.android.material.button.MaterialButton

class MainActivity : AppCompatActivity() {

    private lateinit var markdownInput: EditText
    private lateinit var previewWeb: WebView
    private lateinit var adView: AdView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val toolbar = findViewById<MaterialToolbar>(R.id.toolbar)
        setSupportActionBar(toolbar)

        markdownInput = findViewById(R.id.markdownInput)
        previewWeb = findViewById(R.id.previewWeb)

        previewWeb.settings.javaScriptEnabled = false

        val btnPreview = findViewById<Button>(R.id.btnPreview)
        val btnBold = findViewById<MaterialButton>(R.id.btnBold)
        val btnItalic = findViewById<MaterialButton>(R.id.btnItalic)
        val btnHeading = findViewById<MaterialButton>(R.id.btnHeading)
        val btnLink = findViewById<MaterialButton>(R.id.btnLink)
        val btnCopy = findViewById<MaterialButton>(R.id.btnCopy)
        val btnClear = findViewById<MaterialButton>(R.id.btnClear)

        btnPreview.setOnClickListener {
            val markdown = markdownInput.text.toString()
            val html = convertMarkdownToHtml(markdown)
            val fullHtml = wrapInHtmlTemplate(html)
            previewWeb.loadDataWithBaseURL(null, fullHtml, "text/html", "UTF-8", null)
        }

        btnBold.setOnClickListener {
            wrapSelection("**", "**", "bold")
        }

        btnItalic.setOnClickListener {
            wrapSelection("*", "*", "italic")
        }

        btnHeading.setOnClickListener {
            insertAtLineStart("# ")
        }

        btnLink.setOnClickListener {
            val start = markdownInput.selectionStart
            val end = markdownInput.selectionEnd
            val editable = markdownInput.text
            if (start == end) {
                editable.insert(start, "[text](url)")
            } else {
                val selected = editable.subSequence(start, end).toString()
                editable.replace(start, end, "[$selected](url)")
            }
        }

        btnCopy.setOnClickListener {
            val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
            val clip = ClipData.newPlainText("Markdown", markdownInput.text.toString())
            clipboard.setPrimaryClip(clip)
            Toast.makeText(this, "Markdown copied to clipboard", Toast.LENGTH_SHORT).show()
        }

        btnClear.setOnClickListener {
            markdownInput.text.clear()
            previewWeb.loadDataWithBaseURL(null, "", "text/html", "UTF-8", null)
        }

        MobileAds.initialize(this) {}
        adView = findViewById(R.id.adView)
        val adRequest = AdRequest.Builder().build()
        adView.loadAd(adRequest)
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

    private fun wrapSelection(prefix: String, suffix: String, placeholder: String) {
        val start = markdownInput.selectionStart
        val end = markdownInput.selectionEnd
        val editable = markdownInput.text
        if (start == end) {
            editable.insert(start, "$prefix$placeholder$suffix")
        } else {
            val selected = editable.subSequence(start, end).toString()
            editable.replace(start, end, "$prefix$selected$suffix")
        }
    }

    private fun insertAtLineStart(prefix: String) {
        val start = markdownInput.selectionStart
        val text = markdownInput.text.toString()
        val lineStart = text.lastIndexOf('\n', start - 1) + 1
        markdownInput.text.insert(lineStart, prefix)
    }

    private fun convertMarkdownToHtml(markdown: String): String {
        val lines = markdown.split("\n")
        val result = StringBuilder()
        var inCodeBlock = false
        var inUnorderedList = false
        var inOrderedList = false

        for (line in lines) {
            // Code block toggle
            if (line.trimStart().startsWith("```")) {
                if (inCodeBlock) {
                    result.append("</code></pre>\n")
                    inCodeBlock = false
                } else {
                    closeLists(result, inUnorderedList, inOrderedList)
                    inUnorderedList = false
                    inOrderedList = false
                    result.append("<pre><code>")
                    inCodeBlock = true
                }
                continue
            }

            if (inCodeBlock) {
                result.append(escapeHtml(line)).append("\n")
                continue
            }

            // Horizontal rule
            if (line.trim() == "---" || line.trim() == "***" || line.trim() == "___") {
                closeLists(result, inUnorderedList, inOrderedList)
                inUnorderedList = false
                inOrderedList = false
                result.append("<hr>\n")
                continue
            }

            // Headers
            if (line.startsWith("### ")) {
                closeLists(result, inUnorderedList, inOrderedList)
                inUnorderedList = false
                inOrderedList = false
                result.append("<h3>${processInline(line.removePrefix("### "))}</h3>\n")
                continue
            }
            if (line.startsWith("## ")) {
                closeLists(result, inUnorderedList, inOrderedList)
                inUnorderedList = false
                inOrderedList = false
                result.append("<h2>${processInline(line.removePrefix("## "))}</h2>\n")
                continue
            }
            if (line.startsWith("# ")) {
                closeLists(result, inUnorderedList, inOrderedList)
                inUnorderedList = false
                inOrderedList = false
                result.append("<h1>${processInline(line.removePrefix("# "))}</h1>\n")
                continue
            }

            // Blockquote
            if (line.startsWith("> ")) {
                closeLists(result, inUnorderedList, inOrderedList)
                inUnorderedList = false
                inOrderedList = false
                result.append("<blockquote>${processInline(line.removePrefix("> "))}</blockquote>\n")
                continue
            }

            // Unordered list
            if (line.trimStart().startsWith("- ")) {
                if (inOrderedList) {
                    result.append("</ol>\n")
                    inOrderedList = false
                }
                if (!inUnorderedList) {
                    result.append("<ul>\n")
                    inUnorderedList = true
                }
                result.append("<li>${processInline(line.trimStart().removePrefix("- "))}</li>\n")
                continue
            }

            // Ordered list
            if (line.trimStart().matches(Regex("^\\d+\\.\\s.*"))) {
                if (inUnorderedList) {
                    result.append("</ul>\n")
                    inUnorderedList = false
                }
                if (!inOrderedList) {
                    result.append("<ol>\n")
                    inOrderedList = true
                }
                val content = line.trimStart().replace(Regex("^\\d+\\.\\s"), "")
                result.append("<li>${processInline(content)}</li>\n")
                continue
            }

            // Close any open lists
            closeLists(result, inUnorderedList, inOrderedList)
            inUnorderedList = false
            inOrderedList = false

            // Empty line
            if (line.isBlank()) {
                result.append("<br>\n")
                continue
            }

            // Paragraph
            result.append("<p>${processInline(line)}</p>\n")
        }

        // Close any remaining open elements
        closeLists(result, inUnorderedList, inOrderedList)
        if (inCodeBlock) {
            result.append("</code></pre>\n")
        }

        return result.toString()
    }

    private fun closeLists(result: StringBuilder, inUnorderedList: Boolean, inOrderedList: Boolean) {
        if (inUnorderedList) result.append("</ul>\n")
        if (inOrderedList) result.append("</ol>\n")
    }

    private fun processInline(text: String): String {
        var processed = text

        // Images: ![alt](url)
        processed = processed.replace(Regex("!\\[([^]]*)]\\(([^)]+)\\)")) {
            "<img src=\"${it.groupValues[2]}\" alt=\"${it.groupValues[1]}\">"
        }

        // Links: [text](url)
        processed = processed.replace(Regex("\\[([^]]*)]\\(([^)]+)\\)")) {
            "<a href=\"${it.groupValues[2]}\">${it.groupValues[1]}</a>"
        }

        // Bold: **text**
        processed = processed.replace(Regex("\\*\\*(.+?)\\*\\*")) {
            "<strong>${it.groupValues[1]}</strong>"
        }

        // Italic: *text*
        processed = processed.replace(Regex("\\*(.+?)\\*")) {
            "<em>${it.groupValues[1]}</em>"
        }

        // Inline code: `code`
        processed = processed.replace(Regex("`([^`]+)`")) {
            "<code>${it.groupValues[1]}</code>"
        }

        return processed
    }

    private fun escapeHtml(text: String): String {
        return text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\"", "&quot;")
    }

    private fun wrapInHtmlTemplate(bodyHtml: String): String {
        return """
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {
                    font-family: sans-serif;
                    padding: 12px;
                    line-height: 1.6;
                    color: #333;
                }
                code {
                    background: #f0f0f5;
                    padding: 2px 6px;
                    border-radius: 4px;
                    font-size: 0.9em;
                }
                pre {
                    background: #f0f0f5;
                    padding: 12px;
                    border-radius: 6px;
                    overflow-x: auto;
                }
                pre code {
                    padding: 0;
                    background: none;
                }
                blockquote {
                    border-left: 4px solid #6200EE;
                    margin-left: 0;
                    padding-left: 16px;
                    color: #555;
                }
                img {
                    max-width: 100%;
                    height: auto;
                }
                hr {
                    border: none;
                    border-top: 1px solid #ddd;
                    margin: 16px 0;
                }
                a {
                    color: #6200EE;
                }
            </style>
            </head>
            <body>
            $bodyHtml
            </body>
            </html>
        """.trimIndent()
    }
}
