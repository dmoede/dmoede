package com.dmoede.garytracker

import android.app.DatePickerDialog
import android.os.Bundle
import android.view.inputmethod.InputMethodManager
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.ListView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import java.time.LocalDate

class MainActivity : AppCompatActivity() {

    private lateinit var adapter: ArrayAdapter<String>
    private var entries: List<GaryData.WeightEntry> = emptyList()

    /** Date the next logged weight will be recorded under; defaults to today. */
    private var selectedDate: LocalDate = LocalDate.now()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        adapter = ArrayAdapter(this, R.layout.item_weight, R.id.weight_text, mutableListOf())
        val listView = findViewById<ListView>(R.id.weight_list)
        listView.adapter = adapter

        val dateButton = findViewById<Button>(R.id.date_button)
        updateDateButton()
        dateButton.setOnClickListener { showDatePicker() }

        val input = findViewById<EditText>(R.id.weight_input)
        findViewById<Button>(R.id.log_button).setOnClickListener {
            val lbs = input.text.toString().toDoubleOrNull()
            if (lbs == null || lbs <= 0 || lbs > 200) {
                Toast.makeText(this, getString(R.string.invalid_weight), Toast.LENGTH_SHORT).show()
            } else {
                GaryData.addWeight(this, GaryData.WeightEntry(selectedDate, lbs))
                input.text.clear()
                hideKeyboard(input)
                selectedDate = LocalDate.now()
                updateDateButton()
                refresh()
                GaryWidgetProvider.updateAll(this)
                Toast.makeText(this, getString(R.string.weight_logged), Toast.LENGTH_SHORT).show()
            }
        }

        listView.setOnItemLongClickListener { _, _, position, _ ->
            val entry = entries.asReversed()[position]
            AlertDialog.Builder(this)
                .setTitle(getString(R.string.delete_title))
                .setMessage(getString(R.string.delete_message,
                    GaryData.formatLbs(entry.lbs), GaryData.formatDate(entry.date)))
                .setPositiveButton(R.string.delete) { _, _ ->
                    GaryData.removeWeight(this, entry)
                    refresh()
                    GaryWidgetProvider.updateAll(this)
                }
                .setNegativeButton(android.R.string.cancel, null)
                .show()
            true
        }
    }

    override fun onResume() {
        super.onResume()
        refresh()
    }

    private fun refresh() {
        findViewById<TextView>(R.id.age_text).text = GaryData.ageDescription()
        findViewById<TextView>(R.id.birthday_text).text = getString(
            R.string.born_line, GaryData.formatDate(GaryData.BIRTHDAY), GaryData.ageDays())

        entries = GaryData.getWeights(this)
        val rows = entries.asReversed().mapIndexed { i, entry ->
            val reversed = entries.asReversed()
            val previous = reversed.getOrNull(i + 1)
            val change = if (previous != null) {
                val diff = entry.lbs - previous.lbs
                val sign = if (diff >= 0) "+" else ""
                "  ($sign${String.format("%.1f", diff)})"
            } else ""
            "${GaryData.formatDate(entry.date)}  —  ${GaryData.formatLbs(entry.lbs)}$change"
        }
        adapter.clear()
        adapter.addAll(rows)

        findViewById<TextView>(R.id.empty_text).text =
            if (entries.isEmpty()) getString(R.string.no_weights) else ""
    }

    private fun updateDateButton() {
        val label = if (selectedDate == LocalDate.now()) getString(R.string.date_today)
            else GaryData.formatDateShort(selectedDate)
        findViewById<Button>(R.id.date_button).text = label
    }

    private fun showDatePicker() {
        val dialog = DatePickerDialog(
            this,
            { _, year, month, day ->
                selectedDate = LocalDate.of(year, month + 1, day)
                updateDateButton()
            },
            selectedDate.year,
            selectedDate.monthValue - 1,
            selectedDate.dayOfMonth
        )
        // Can't weigh him before he was born, or in the future.
        dialog.datePicker.minDate =
            GaryData.BIRTHDAY.toEpochDay() * 24L * 60L * 60L * 1000L
        dialog.datePicker.maxDate = System.currentTimeMillis()
        dialog.show()
    }

    private fun hideKeyboard(view: EditText) {
        val imm = getSystemService(INPUT_METHOD_SERVICE) as InputMethodManager
        imm.hideSoftInputFromWindow(view.windowToken, 0)
    }
}
