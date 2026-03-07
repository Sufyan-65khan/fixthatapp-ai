package com.fixthatapp.errorexplainer

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.net.Uri
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.gms.ads.AdRequest
import com.google.android.gms.ads.AdView
import com.google.android.gms.ads.MobileAds
import com.google.android.material.appbar.MaterialToolbar
import com.google.android.material.button.MaterialButton
import com.google.android.material.card.MaterialCardView

data class ErrorInfo(
    val pattern: String,
    val severity: String,
    val explanation: String,
    val fix: String,
    val related: String
)

class MainActivity : AppCompatActivity() {

    private lateinit var errorInput: EditText
    private lateinit var btnExplain: Button
    private lateinit var btnPreset404: Button
    private lateinit var btnPresetNull: Button
    private lateinit var btnPresetPerm: Button
    private lateinit var btnPresetOOM: Button
    private lateinit var resultCard: MaterialCardView
    private lateinit var severityText: TextView
    private lateinit var explanationText: TextView
    private lateinit var fixText: TextView
    private lateinit var relatedText: TextView
    private lateinit var btnCopy: MaterialButton
    private lateinit var btnClear: MaterialButton
    private lateinit var adView: AdView

    private val errorDatabase = listOf(
        ErrorInfo(
            pattern = "404|not found",
            severity = "Medium",
            explanation = "The requested resource could not be found on the server. This usually means the URL is incorrect, the resource has been moved or deleted, or the API endpoint does not exist.",
            fix = "Check the URL for typos. Verify the resource exists on the server. If it's an API, confirm the endpoint path is correct and the resource ID is valid. Check if the resource has been moved to a different URL.",
            related = "410 Gone, 301 Moved Permanently, 400 Bad Request"
        ),
        ErrorInfo(
            pattern = "500|internal server error",
            severity = "High",
            explanation = "The server encountered an unexpected condition that prevented it from fulfilling the request. This is a server-side error, meaning the problem is not with your code or request, but with the server itself.",
            fix = "Check the server logs for detailed error information. Verify that the server application is running correctly. Check for database connectivity issues. Ensure all server-side dependencies are available and properly configured.",
            related = "502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout"
        ),
        ErrorInfo(
            pattern = "403|forbidden",
            severity = "Medium",
            explanation = "The server understood the request but refuses to authorize it. You do not have permission to access the requested resource, even though your identity may be known to the server.",
            fix = "Check your access permissions for the resource. Verify your API key or authentication token has the required scopes. Contact the resource owner to request access. Check if IP-based restrictions are blocking your request.",
            related = "401 Unauthorized, 407 Proxy Authentication Required"
        ),
        ErrorInfo(
            pattern = "401|unauthorized",
            severity = "Medium",
            explanation = "The request requires user authentication. Either no credentials were provided, or the provided credentials are invalid or expired.",
            fix = "Provide valid authentication credentials (API key, token, or username/password). Check if your token has expired and refresh it. Ensure the Authorization header is correctly formatted. Verify your account is active.",
            related = "403 Forbidden, 407 Proxy Authentication Required, 419 Session Expired"
        ),
        ErrorInfo(
            pattern = "nullpointerexception|null pointer|null reference",
            severity = "High",
            explanation = "Your code attempted to use a reference that points to no object (null). This happens when you try to call a method, access a field, or use an object that hasn't been initialized or has been set to null.",
            fix = "Add null checks before using objects. Use Kotlin's null safety features (?. and ?:). Initialize variables before use. Use 'let' or 'also' for safe null handling. Check method return values for null before using them.",
            related = "KotlinNullPointerException, IllegalStateException, UninitializedPropertyAccessException"
        ),
        ErrorInfo(
            pattern = "outofmemoryerror|oom|heap space",
            severity = "Critical",
            explanation = "The Java Virtual Machine (JVM) cannot allocate an object because it is out of memory, and no more memory could be made available by the garbage collector. Your application is consuming more memory than allocated.",
            fix = "Optimize memory usage by releasing unused references. Use memory-efficient data structures. Avoid loading large files entirely into memory—use streams instead. Check for memory leaks using a profiler. Increase heap size with -Xmx flag if appropriate.",
            related = "GC Overhead Limit Exceeded, Direct Buffer Memory, Metaspace"
        ),
        ErrorInfo(
            pattern = "stackoverflowerror|stack overflow",
            severity = "Critical",
            explanation = "The application has exhausted its call stack, usually due to infinite or excessively deep recursion. Each method call adds a frame to the stack, and when the stack is full, this error occurs.",
            fix = "Check recursive methods for a proper base case that terminates the recursion. Convert deep recursion to iterative solutions using loops. Increase stack size with -Xss flag only as a temporary measure. Check for circular method calls.",
            related = "RecursionError, InfiniteLoopException"
        ),
        ErrorInfo(
            pattern = "classnotfoundexception|class not found|noclassdeffounderror",
            severity = "High",
            explanation = "The JVM cannot find the specified class at runtime. This means the class exists at compile time but is missing from the classpath when the application runs.",
            fix = "Verify all dependencies are included in your build configuration (build.gradle). Check that the class name and package are spelled correctly. Ensure the JAR or AAR containing the class is on the classpath. Clean and rebuild the project.",
            related = "NoClassDefFoundError, ClassCastException, LinkageError"
        ),
        ErrorInfo(
            pattern = "filenotfoundexception|file not found|no such file",
            severity = "Medium",
            explanation = "The system cannot find the file at the specified path. The file may not exist, the path may be incorrect, or the application may not have permission to access the file's directory.",
            fix = "Verify the file path is correct and the file exists. Check file name spelling and case sensitivity. Ensure the application has read permissions for the directory. Use absolute paths or verify the working directory for relative paths.",
            related = "IOException, AccessDeniedException, NoSuchFileException"
        ),
        ErrorInfo(
            pattern = "ioexception|i/o error|input/output",
            severity = "Medium",
            explanation = "An I/O (Input/Output) operation has failed or been interrupted. This is a general exception for various I/O failures such as reading/writing files, network communication, or stream operations.",
            fix = "Check if the file or resource exists and is accessible. Verify network connectivity for network-related I/O. Ensure streams are properly closed using try-with-resources or use/finally blocks. Check disk space if writing files.",
            related = "FileNotFoundException, SocketException, EOFException"
        ),
        ErrorInfo(
            pattern = "permission denied|eacces|access denied",
            severity = "Medium",
            explanation = "The operation was rejected because the current user or process does not have the required permissions. This can occur at the OS level, file system level, or application level.",
            fix = "Check and update file/directory permissions using chmod. On Android, request runtime permissions in your app. Verify the user account has necessary privileges. Check SELinux or AppArmor policies on Linux systems.",
            related = "SecurityException, AccessControlException, 403 Forbidden"
        ),
        ErrorInfo(
            pattern = "connection refused|econnrefused",
            severity = "Medium",
            explanation = "The connection attempt was rejected by the target machine. This usually means no application is listening on the specified port, or a firewall is blocking the connection.",
            fix = "Verify the target server or service is running. Check the hostname and port number are correct. Ensure no firewall rules are blocking the connection. Check if the server has reached its connection limit. Try connecting from a different network.",
            related = "Connection timed out, ECONNRESET, EHOSTUNREACH"
        ),
        ErrorInfo(
            pattern = "timeout|timed out|deadline exceeded",
            severity = "Medium",
            explanation = "The operation did not complete within the allowed time period. This can happen with network requests, database queries, or any operation with a time limit.",
            fix = "Increase the timeout duration if the operation legitimately needs more time. Optimize the slow operation (query optimization, reducing payload size). Check network latency and connectivity. Implement retry logic with exponential backoff.",
            related = "SocketTimeoutException, ConnectTimeoutException, 504 Gateway Timeout"
        ),
        ErrorInfo(
            pattern = "ssl|certificate|tls|handshake",
            severity = "High",
            explanation = "An SSL/TLS error occurred during secure communication. This could be due to an expired certificate, self-signed certificate, certificate hostname mismatch, or incompatible TLS versions.",
            fix = "Check if the server's SSL certificate is valid and not expired. Ensure the certificate matches the hostname. Update your trusted CA certificates. Do not disable SSL verification in production. Check for TLS version compatibility.",
            related = "CertificateException, SSLPeerUnverifiedException, CERTIFICATE_VERIFY_FAILED"
        ),
        ErrorInfo(
            pattern = "cors|cross-origin|access-control-allow-origin",
            severity = "Medium",
            explanation = "The browser blocked a cross-origin request because the server's CORS (Cross-Origin Resource Sharing) policy does not allow it. This is a browser security feature that restricts web pages from making requests to a different domain.",
            fix = "Configure the server to include proper CORS headers (Access-Control-Allow-Origin). Add the requesting domain to the allowed origins list. For development, use a CORS proxy or browser extension. Ensure preflight OPTIONS requests are handled.",
            related = "Preflight request failed, Mixed content, Content Security Policy"
        ),
        ErrorInfo(
            pattern = "syntaxerror|syntax error|unexpected token",
            severity = "Low",
            explanation = "The code contains a syntax error that prevents it from being parsed correctly. This means the code structure violates the language's grammar rules.",
            fix = "Check for missing or extra brackets, parentheses, or braces. Look for missing semicolons or commas. Verify string quotes are properly matched. Use an IDE or linter to highlight syntax issues. Check for invalid characters in the code.",
            related = "ParseError, CompilationError, UnexpectedTokenException"
        ),
        ErrorInfo(
            pattern = "typeerror|type error|type mismatch",
            severity = "Medium",
            explanation = "An operation was performed on a value of the wrong type. For example, calling a method on undefined, using a string where a number is expected, or passing the wrong argument types to a function.",
            fix = "Check the types of variables and function arguments. Use type checking or type assertions. Verify that objects have the expected properties before accessing them. Use TypeScript or type annotations to catch type errors at compile time.",
            related = "ClassCastException, InvalidCastException, ArgumentTypeError"
        ),
        ErrorInfo(
            pattern = "referenceerror|undefined is not|is not defined",
            severity = "Medium",
            explanation = "A variable or function was referenced that has not been declared or is out of scope. This means the code is trying to use something that doesn't exist in the current context.",
            fix = "Check that the variable or function name is spelled correctly. Ensure the variable is declared before use. Verify the variable is in the correct scope. Check import statements if using modules. Avoid using variables before their declaration.",
            related = "NameError, UndeclaredIdentifierError, ScopeError"
        ),
        ErrorInfo(
            pattern = "arrayindexoutofbounds|index out of bounds|indexoutofrange|array index",
            severity = "Medium",
            explanation = "The code tried to access an array or list element at an index that is outside the valid range. Arrays are zero-indexed, so valid indices range from 0 to length-1.",
            fix = "Check the array length before accessing elements. Use bounds checking or safe access methods. Verify loop conditions don't exceed array bounds. Use forEach or iterators instead of index-based access when possible.",
            related = "StringIndexOutOfBoundsException, IndexOutOfBoundsException, RangeError"
        ),
        ErrorInfo(
            pattern = "concurrentmodificationexception|concurrent modification",
            severity = "High",
            explanation = "A collection was modified while it was being iterated over. This typically happens when you add or remove elements from a list, set, or map inside a for-each loop that is iterating over that same collection.",
            fix = "Use an Iterator and its remove() method instead of modifying the collection directly. Create a copy of the collection to iterate over. Use ConcurrentHashMap or CopyOnWriteArrayList for thread-safe collections. Collect modifications and apply them after iteration.",
            related = "ConcurrentModificationException, UnsupportedOperationException"
        ),
        ErrorInfo(
            pattern = "numberformatexception|number format|cannot parse",
            severity = "Low",
            explanation = "A string was attempted to be converted to a numeric type, but the string does not contain a valid number. For example, trying to parse 'abc' as an integer.",
            fix = "Validate input strings before parsing. Use tryParse or toIntOrNull() methods that return null instead of throwing. Trim whitespace from input strings. Check for non-numeric characters. Handle the exception with a try-catch block and provide user feedback.",
            related = "ParseException, FormatException, ValueError"
        ),
        ErrorInfo(
            pattern = "illegalargumentexception|illegal argument|invalid argument",
            severity = "Medium",
            explanation = "A method received an argument that is not valid or not within the expected range. The method's contract specifies what arguments are acceptable, and the provided argument violated that contract.",
            fix = "Check the method's documentation for valid argument ranges and types. Validate arguments before passing them to methods. Use require() or check() functions for precondition validation. Ensure enum values and constants are valid.",
            related = "IllegalStateException, InvalidParameterException, ArgumentException"
        ),
        ErrorInfo(
            pattern = "unsupportedoperationexception|unsupported operation|not supported",
            severity = "Medium",
            explanation = "The requested operation is not supported by the object or implementation. This often occurs when using immutable collections or when a subclass doesn't implement an inherited method.",
            fix = "Check if you're using an immutable collection that doesn't support modification. Use a mutable version of the collection (e.g., mutableListOf instead of listOf). Verify the implementation supports the operation you're calling.",
            related = "NotImplementedError, AbstractMethodError, ReadOnlyBufferException"
        ),
        ErrorInfo(
            pattern = "segmentation fault|segfault|sigsegv|signal 11",
            severity = "Critical",
            explanation = "The program tried to access a memory location that it is not allowed to access. This is a severe error typically caused by dereferencing a null or invalid pointer, buffer overflows, or accessing freed memory.",
            fix = "Check for null pointer dereferences. Verify array bounds in C/C++ code. Use memory sanitizers (AddressSanitizer) to detect memory issues. Check for use-after-free bugs. Ensure pointers are initialized before use. Use smart pointers in C++.",
            related = "SIGBUS, SIGABRT, Access Violation, EXC_BAD_ACCESS"
        ),
        ErrorInfo(
            pattern = "enomem|cannot allocate|out of memory|memory allocation failed",
            severity = "Critical",
            explanation = "The system does not have enough memory to complete the requested allocation. The process has either exhausted its available memory or the system is running low on physical and virtual memory.",
            fix = "Free unused memory and close unnecessary applications. Optimize data structures to use less memory. Process large datasets in smaller chunks. Check for memory leaks using profiling tools. Consider increasing swap space or system RAM.",
            related = "OutOfMemoryError, std::bad_alloc, SIGKILL (OOM Killer)"
        )
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        MobileAds.initialize(this) {}

        val toolbar = findViewById<MaterialToolbar>(R.id.toolbar)
        setSupportActionBar(toolbar)

        errorInput = findViewById(R.id.errorInput)
        btnExplain = findViewById(R.id.btnExplain)
        btnPreset404 = findViewById(R.id.btnPreset404)
        btnPresetNull = findViewById(R.id.btnPresetNull)
        btnPresetPerm = findViewById(R.id.btnPresetPerm)
        btnPresetOOM = findViewById(R.id.btnPresetOOM)
        resultCard = findViewById(R.id.resultCard)
        severityText = findViewById(R.id.severityText)
        explanationText = findViewById(R.id.explanationText)
        fixText = findViewById(R.id.fixText)
        relatedText = findViewById(R.id.relatedText)
        btnCopy = findViewById(R.id.btnCopy)
        btnClear = findViewById(R.id.btnClear)
        adView = findViewById(R.id.adView)

        val adRequest = AdRequest.Builder().build()
        adView.loadAd(adRequest)

        btnExplain.setOnClickListener {
            explainError()
        }

        btnPreset404.setOnClickListener {
            errorInput.setText("HTTP 404 Not Found")
            explainError()
        }

        btnPresetNull.setOnClickListener {
            errorInput.setText("java.lang.NullPointerException: Attempt to invoke virtual method on a null object reference")
            explainError()
        }

        btnPresetPerm.setOnClickListener {
            errorInput.setText("Permission denied (EACCES)")
            explainError()
        }

        btnPresetOOM.setOnClickListener {
            errorInput.setText("java.lang.OutOfMemoryError: Failed to allocate")
            explainError()
        }

        btnCopy.setOnClickListener {
            copyExplanation()
        }

        btnClear.setOnClickListener {
            clearAll()
        }
    }

    private fun explainError() {
        val input = errorInput.text.toString().trim()
        if (input.isEmpty()) {
            Toast.makeText(this, "Please enter an error message", Toast.LENGTH_SHORT).show()
            return
        }

        val inputLower = input.lowercase()
        var matchedError: ErrorInfo? = null

        for (error in errorDatabase) {
            val patterns = error.pattern.split("|")
            for (pattern in patterns) {
                if (inputLower.contains(pattern.lowercase())) {
                    matchedError = error
                    break
                }
            }
            if (matchedError != null) break
        }

        resultCard.visibility = View.VISIBLE

        if (matchedError != null) {
            severityText.text = "Severity: ${matchedError.severity}"
            severityText.setTextColor(getSeverityColor(matchedError.severity))
            explanationText.text = matchedError.explanation
            fixText.text = matchedError.fix
            relatedText.text = matchedError.related
        } else {
            severityText.text = "Severity: Unknown"
            severityText.setTextColor(Color.GRAY)
            explanationText.text = "This error is not in our database yet. Try searching online for the exact error message."
            fixText.text = "Copy the error message and search it on Google or Stack Overflow for community solutions."
            relatedText.text = "N/A"
        }
    }

    private fun getSeverityColor(severity: String): Int {
        return when (severity) {
            "Critical" -> Color.parseColor("#D32F2F")
            "High" -> Color.parseColor("#F57C00")
            "Medium" -> Color.parseColor("#FBC02D")
            "Low" -> Color.parseColor("#388E3C")
            else -> Color.GRAY
        }
    }

    private fun copyExplanation() {
        if (resultCard.visibility != View.VISIBLE) {
            Toast.makeText(this, "No explanation to copy", Toast.LENGTH_SHORT).show()
            return
        }

        val text = buildString {
            appendLine("Severity: ${severityText.text}")
            appendLine()
            appendLine("What this means:")
            appendLine(explanationText.text)
            appendLine()
            appendLine("How to fix:")
            appendLine(fixText.text)
            appendLine()
            appendLine("Related errors:")
            appendLine(relatedText.text)
        }

        val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        val clip = ClipData.newPlainText("Error Explanation", text)
        clipboard.setPrimaryClip(clip)
        Toast.makeText(this, "Explanation copied to clipboard", Toast.LENGTH_SHORT).show()
    }

    private fun clearAll() {
        errorInput.text.clear()
        resultCard.visibility = View.GONE
        severityText.text = ""
        explanationText.text = ""
        fixText.text = ""
        relatedText.text = ""
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menu.add(0, 1, 0, "Privacy Policy")
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
