package com.dmoede.garytracker

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject
import java.time.LocalDate
import java.time.Period
import java.time.format.DateTimeFormatter
import java.time.temporal.ChronoUnit

object GaryData {

    val BIRTHDAY: LocalDate = LocalDate.of(2026, 5, 6)

    private const val PREFS = "gary_tracker"
    private const val KEY_WEIGHTS = "weights"

    data class WeightEntry(val date: LocalDate, val lbs: Double)

    fun ageDays(today: LocalDate = LocalDate.now()): Long =
        ChronoUnit.DAYS.between(BIRTHDAY, today)

    /** e.g. "9 weeks, 3 days old" while a young puppy, then months, then years. */
    fun ageDescription(today: LocalDate = LocalDate.now()): String {
        val days = ageDays(today)
        if (days < 0) return "Not born yet!"
        val period = Period.between(BIRTHDAY, today)
        val months = period.toTotalMonths()
        return when {
            days < 7 * 16 -> {
                val weeks = days / 7
                val rem = days % 7
                if (rem == 0L) "$weeks ${plural(weeks, "week")} old"
                else "$weeks ${plural(weeks, "week")}, $rem ${plural(rem, "day")} old"
            }
            months < 24 -> {
                val d = period.days.toLong()
                if (d == 0L) "$months ${plural(months, "month")} old"
                else "$months ${plural(months, "month")}, $d ${plural(d, "day")} old"
            }
            else -> {
                val y = period.years.toLong()
                val m = (period.months).toLong()
                if (m == 0L) "$y ${plural(y, "year")} old"
                else "$y ${plural(y, "year")}, $m ${plural(m, "month")} old"
            }
        }
    }

    /** Compact form for the widget, e.g. "9w 3d" or "14m". */
    fun ageShort(today: LocalDate = LocalDate.now()): String {
        val days = ageDays(today)
        if (days < 0) return "–"
        val months = Period.between(BIRTHDAY, today).toTotalMonths()
        return when {
            days < 7 * 16 -> "${days / 7}w ${days % 7}d"
            months < 24 -> "${months}mo"
            else -> {
                val p = Period.between(BIRTHDAY, today)
                "${p.years}y ${p.months}mo"
            }
        }
    }

    fun getWeights(context: Context): List<WeightEntry> {
        val raw = prefs(context).getString(KEY_WEIGHTS, "[]") ?: "[]"
        val array = JSONArray(raw)
        val list = ArrayList<WeightEntry>(array.length())
        for (i in 0 until array.length()) {
            val obj = array.getJSONObject(i)
            list.add(WeightEntry(LocalDate.parse(obj.getString("date")), obj.getDouble("lbs")))
        }
        list.sortBy { it.date }
        return list
    }

    fun addWeight(context: Context, entry: WeightEntry) {
        // One entry per day: a new weigh-in on the same date replaces the old one.
        val list = getWeights(context).filter { it.date != entry.date } + entry
        saveWeights(context, list.sortedBy { it.date })
    }

    fun removeWeight(context: Context, entry: WeightEntry) {
        saveWeights(context, getWeights(context).filter { it != entry })
    }

    fun latestWeight(context: Context): WeightEntry? = getWeights(context).lastOrNull()

    fun formatDate(date: LocalDate): String =
        date.format(DateTimeFormatter.ofPattern("MMM d, yyyy"))

    fun formatDateShort(date: LocalDate): String =
        date.format(DateTimeFormatter.ofPattern("MMM d"))

    fun formatLbs(lbs: Double): String =
        if (lbs == lbs.toLong().toDouble()) "${lbs.toLong()} lbs" else "$lbs lbs"

    private fun saveWeights(context: Context, list: List<WeightEntry>) {
        val array = JSONArray()
        for (entry in list) {
            array.put(JSONObject().put("date", entry.date.toString()).put("lbs", entry.lbs))
        }
        prefs(context).edit().putString(KEY_WEIGHTS, array.toString()).apply()
    }

    private fun prefs(context: Context) =
        context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)

    private fun plural(n: Long, word: String) = if (n == 1L) word else "${word}s"
}
